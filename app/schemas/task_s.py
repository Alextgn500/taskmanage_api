from pydantic import BaseModel, ConfigDict
from typing import Optional


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    priority: int
    completed: bool
    user_id: int
    slug: str


class CreateTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
    priority: int
    completed: bool = False
    user_id: int

class UpdateTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    content: str | None = None
    priority: int | None = None
    completed: bool | None = None
    user_id: int | None = None  # Сделать необязательным



class TaskResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Пример задачи",
                "content": "Это содержание задачи",
                "priority": 3,
                "completed": False,
                "user_id": 42,
                "slug": "primer-zadachi"
            }
        }
    )

    id: int
    title: str
    content: str
    priority: int
    completed: bool
    user_id: int
    slug: str