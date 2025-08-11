from pydantic import BaseModel, field_validator, ConfigDict
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


class CreateUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    firstname: str
    lastname: str
    age: int
    password: str

    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        if v < 0:
            raise ValueError('Возраст не может быть отрицательным')
        if v > 120:
            raise ValueError('Возраст не может быть больше 120')
        return v


class UpdateUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: Optional[str] =None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = None
    password: Optional[str]= None


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "john_doe",
                "firstname": "John",
                "lastname": "Doe",
                "age": 30,
                "slug": "john-doe"
            }
        }
    )

    id: int
    username: str
    firstname: str
    lastname: str
    age: int
    slug: str
