import pytest
from app.models.user_m import Users


@pytest.mark.asyncio
async def test_user_creation_in_db(db_session):
    """Тест создания пользователя в БД"""
    user = Users(
        username="testuser",
        firstname="Test",
        lastname="User",
        age=25,
        slug="test-user",
        password="hashed_password"
    )

    db_session.add(user)
    await db_session.commit()

    # Обновляем объект после коммита
    await db_session.refresh(user)

    assert user.id is not None
    assert user.username == "testuser"

