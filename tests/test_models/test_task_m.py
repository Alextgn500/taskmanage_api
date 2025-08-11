import pytest
from pydantic import ValidationError
from app.schemas.task_s import Task, CreateTask, TaskResponse


def test_create_task_valid_data():
    """Тест создания задачи с валидными данными"""
    task_data = {
        "title": "Test Task",
        "content": "This is a test task content",
        "priority": 1,
        "completed": False,
        "user_id": 1
    }

    task = CreateTask(**task_data)

    assert task.title == "Test Task"
    assert task.content == "This is a test task content"
    assert task.priority == 1
    assert task.completed == False
    assert task.user_id == 1


def test_create_task_missing_required_fields():
    """Тест обязательных полей"""
    task_data = {
        "title": "Test Task"
        # Пропущены обязательные поля
    }

    with pytest.raises(ValidationError):
        CreateTask(**task_data)


def test_create_task_invalid_types():
    """Тест неправильных типов данных"""
    task_data = {
        "title": "Test Task",
        "content": "Test content",
        "priority": "not_an_integer",  # Должно быть int
        "completed": False,
        "user_id": 1
    }

    with pytest.raises(ValidationError):
        CreateTask(**task_data)


def test_task_response_model():
    """Тест модели ответа TaskResponse"""
    task_data = {
        "id": 1,
        "title": "Response Task",
        "content": "Task response content",
        "priority": 2,
        "completed": True,
        "user_id": 1,
        "slug": "response-task"
    }

    task = TaskResponse(**task_data)

    assert task.id == 1
    assert task.title == "Response Task"
    assert task.content == "Task response content"
    assert task.priority == 2
    assert task.completed == True
    assert task.user_id == 1
    assert task.slug == "response-task"


def test_task_model_full():
    """Тест полной модели Task"""
    task_data = {
        "id": 1,
        "title": "Full Task",
        "content": "Full task content",
        "priority": 3,
        "completed": False,
        "user_id": 1,
        "slug": "full-task"
    }

    task = Task(**task_data)

    assert task.id == 1
    assert task.title == "Full Task"
    assert task.content == "Full task content"
    assert task.priority == 3
    assert task.completed == False
    assert task.user_id == 1
    assert task.slug == "full-task"


def test_create_task_different_priorities():
    """Тест разных приоритетов"""
    priorities = [1, 2, 3, 4, 5]

    for priority in priorities:
        task_data = {
            "title": f"Task Priority {priority}",
            "content": f"Task with priority {priority}",
            "priority": priority,
            "completed": False,
            "user_id": 1
        }

        task = CreateTask(**task_data)
        assert task.priority == priority


def test_create_task_completed_status():
    """Тест статуса выполнения задачи"""
    task_data = {
        "title": "Status Test Task",
        "content": "Testing completion status",
        "priority": 1,
        "completed": True,
        "user_id": 1
    }

    task = CreateTask(**task_data)
    assert task.completed == True

    # Изменим статус
    task_data["completed"] = False
    task = CreateTask(**task_data)
    assert task.completed == False