from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.task_s import TaskResponse, CreateTask
from app.backend.db_depends import get_async_db
from app.services import tasks

router_task = APIRouter(prefix='/tasks', tags=['tasks'])


@router_task.get("/", response_model=List[TaskResponse])
async def all_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_async_db)):
    return await tasks.get_all_tasks(skip, limit, db)


@router_task.get("/{task_id}", response_model=TaskResponse)
async def task_by_id(task_id: int, db: Session = Depends(get_async_db)):
    return await tasks.get_task_by_id(task_id, db)


@router_task.post("/", response_model=TaskResponse)
async def create_task(task: CreateTask, db: Session = Depends(get_async_db)):
    return await tasks.create_task(task, db)


@router_task.put("/{task_id}", response_model=TaskResponse)
async def update_task_route(task_id: int, task: CreateTask, db: Session = Depends(get_async_db)):
    return await tasks.update_task(task_id, task, db)


@router_task.delete("/{task_id}", response_model=dict)
async def delete_task_route(task_id: int, db: Session = Depends(get_async_db)):
    return await tasks.delete_task(task_id, db)

