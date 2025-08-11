import pytest
from fastapi.testclient import TestClient


def test_get_all_tasks(test_client):
    """Тест GET /tasks/ - получение всех задач"""
    response = test_client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_task(test_client, test_user_data):
    """Тест POST /tasks/ - создание задачи"""
    # Сначала создаем пользователя
    user_response = test_client.post("/users/", json=test_user_data)
    user_id = user_response.json()["id"]

    # Создаем задачу
    task_data = {
        "title": "Тестовая задача",
        "content": "Описание тестовой задачи",
        "priority": 1,
        "user_id": user_id
    }

    response = test_client.post("/tasks/", json=task_data)
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["title"] == task_data["title"]
    assert data["user_id"] == user_id


def test_get_task_by_id(test_client, test_user_data):
    """Тест GET /tasks/{task_id} - получение задачи по ID"""
    # Создаем пользователя
    user_response = test_client.post("/users/", json=test_user_data)
    user_id = user_response.json()["id"]

    # Создаем задачу
    task_data = {
        "title": "Тестовая задача",
        "content": "Описание тестовой задачи",
        "priority": 1,
        "user_id": user_id
    }

    create_response = test_client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Получаем задачу по ID
    response = test_client.get(f"/tasks/{task_id}")
    assert response.status_code == 200

    task = response.json()
    assert task["id"] == task_id
    assert task["title"] == task_data["title"]


def test_update_task(test_client, test_user_data):
    """Тест PUT /tasks/{task_id} - обновление задачи"""
    # Создаем пользователя
    user_response = test_client.post("/users/", json=test_user_data)
    user_id = user_response.json()["id"]

    # Создаем задачу
    task_data = {
        "title": "Тестовая задача",
        "content": "Описание тестовой задачи",
        "priority": 1,
        "user_id": user_id
    }

    create_response = test_client.post("/tasks/", json=task_data)
    print(f"Create response: {create_response.status_code}, {create_response.json()}")  # ОТЛАДКА
    task_id = create_response.json()["id"]

    # Обновляем задачу
    update_data = {
        "title": "Обновленная задача",
        "content": "Новое описание",
        "priority": 2,
        "completed": True
    }

    print(f"Task ID: {task_id}")  # ОТЛАДКА
    print(f"Update data: {update_data}")  # ОТЛАДКА

    response = test_client.put(f"/tasks/{task_id}", json=update_data)

    print(f"Update response status: {response.status_code}")  # ОТЛАДКА
    print(f"Update response body: {response.json()}")  # ОТЛАДКА

    assert response.status_code == 200


def test_delete_task(test_client, test_user_data):
    """Тест DELETE /tasks/{task_id} - удаление задачи"""
    # Создаем пользователя
    user_response = test_client.post("/users/", json=test_user_data)
    user_id = user_response.json()["id"]

    # Создаем задачу
    task_data = {
        "title": "Тестовая задача",
        "content": "Описание тестовой задачи",
        "priority": 1,
        "user_id": user_id
    }

    create_response = test_client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Удаляем задачу
    response = test_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    # Проверяем, что задача удалена
    get_response = test_client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_task(test_client):
    """Тест GET /tasks/{task_id} - получение несуществующей задачи"""
    response = test_client.get("/tasks/999")
    assert response.status_code == 404
