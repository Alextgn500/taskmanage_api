from pydantic import BaseModel
from  typing import Optional


# Модели Pydantic
class Task(BaseModel):
    id: int
    title: str
    content: str
    priority: int
    completed: bool
    user_id: int
    slug: str

    class Config:
        from_attributes = True


class CreateTask(BaseModel):
    title: str
    content: str
    priority: int
    completed: bool
    user_id: int

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    id: int
    title: str
    content: str
    priority: int
    completed: bool
    user_id: int
    slug: str

    class Config:
        from_attributes = True
        json_schema_extra = {
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
