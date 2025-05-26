from pydantic import BaseModel
from typing import Optional


# Pydantic модели
class User(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    age: int
    slug: str

    class Config:
        from_attribute = True


class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

    class Config:
        from_attributes = True



class UpdateUser(BaseModel):
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = None
    user_id: int

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    age: int
    slug: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "firstname": "John",
                "lastname": "Doe",
                "age": 30,
                "slug": "john-doe"
            }
        }