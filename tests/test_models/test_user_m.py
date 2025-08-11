import pytest
from pydantic import ValidationError
from app.schemas.user_s import CreateUser, UserResponse


def test_create_user_valid_data():
    """Тест создания пользователя с валидными данными"""
    user_data = {
        "username": "testuser",
        "firstname": "Test",
        "lastname": "User",
        "age": 25,
        "password": "password123"
    }

    user = CreateUser(**user_data)

    assert user.username == "testuser"
    assert user.firstname == "Test"
    assert user.lastname == "User"
    assert user.age == 25
    assert user.password == "password123"


def test_create_user_invalid_age():
    """Тест валидации возраста"""
    user_data = {
        "username": "testuser",
        "firstname": "Test",
        "lastname": "User",
        "age": -5,  # Невалидный возраст
        "password": "password123"
    }

    with pytest.raises(ValidationError) as exc_info:
        CreateUser(**user_data)

    assert "Возраст не может быть отрицательным" in str(exc_info.value)


def test_create_user_missing_required_fields():
    """Тест обязательных полей"""
    user_data = {
        "username": "testuser"
        # Пропущены обязательные поля
    }

    with pytest.raises(ValidationError):
        CreateUser(**user_data)


def test_user_response_model():
    """Тест модели ответа (без пароля)"""
    user_data = {
        "id": 1,
        "username": "testuser",
        "firstname": "Test",
        "lastname": "User",
        "age": 25,
        "slug": "test-user"
    }

    user = UserResponse(**user_data)

    assert user.id == 1
    assert user.username == "testuser"
    assert user.firstname == "Test"
    assert user.lastname == "User"
    assert user.age == 25
    assert user.slug == "test-user"
