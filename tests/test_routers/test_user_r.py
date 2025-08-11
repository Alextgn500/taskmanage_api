import pytest
from fastapi.testclient import TestClient



def test_get_all_users(test_client, db_session, test_user_data):
    """Тест GET / - получение всех пользователей"""
    response = test_client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user(test_client, test_user_data):
    """Тест POST / - создание пользователя"""
    response = test_client.post("/users/", json=test_user_data)

    # Исправлено: ожидаем 201
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["username"] == test_user_data["username"]

def test_get_user_by_id(test_client, db_session, test_user_data):
    """Тест GET /{user_id} - получение пользователя по ID"""
    # Создаем пользователя
    create_response = test_client.post("/users/", json=test_user_data)

    # Проверяем, какие поля есть в ответе
    user_data = create_response.json()
    print(f"Create response: {user_data}")

    # Используем ID, если он есть, или берем первого пользователя
    if "id" in user_data:
        user_id = user_data["id"]
    else:
        # Получаем всех пользователей и берем первого
        all_users = test_client.get("/users/").json()
        user_id = all_users[0]["id"] if all_users else 1

    # Получаем пользователя по ID
    response = test_client.get(f"/users/{user_id}")
    assert response.status_code == 200


def test_update_user(test_client, test_user_data):
    """Тест PUT /{user_id} - обновление пользователя"""
    create_response = test_client.post("/users/", json=test_user_data)
    assert create_response.status_code == 201

    create_data = create_response.json()
    print(f"Create response: {create_data}")  # Отладка

    # Проверяем наличие ID
    if "id" not in create_data:
        pytest.fail(f"ID отсутствует в ответе создания: {create_data}")

    user_id = create_data["id"]

    # Полные данные для обновления
    update_data = {
        "username": "updateduser",
        "firstname": "Updated",
        "lastname": "UpdatedLast",
        "age": 30,
        "password": "newpassword"
    }

    response = test_client.put(f"/users/{user_id}", json=update_data)

    print(f"Update status: {response.status_code}")  # Отладка
    print(f"Update response: {response.json()}")  # Отладка

    if response.status_code != 200:
        pytest.fail(f"Ошибка обновления: {response.json()}")

    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["firstname"] == "Updated"
    assert updated_user["age"] == 30


def test_delete_user(test_client, test_user_data):
    """Тест DELETE /{user_id} - удаление пользователя"""
    create_response = test_client.post("/users/", json=test_user_data)
    assert create_response.status_code == 201

    create_data = create_response.json()

    if "id" not in create_data:
        pytest.fail(f"ID отсутствует в ответе создания: {create_data}")

    user_id = create_data["id"]

    # Удаляем пользователя
    response = test_client.delete(f"/users/{user_id}")

    print(f"Delete status: {response.status_code}")  # Отладка
    print(f"Delete response: {response.json()}")  # Отладка

    assert response.status_code == 200

    # Проверяем, что пользователь удален
    get_response = test_client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_user(test_client):
    """Тест получения несуществующего пользователя"""
    response = test_client.get("/users/9999")
    assert response.status_code == 404
