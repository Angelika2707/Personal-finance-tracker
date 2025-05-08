import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from app.database.models import User
from app.api.users.schemas import UserCreate
from app.api.users.crud import create_user, get_user_by_username


@pytest.fixture
def session():
    return AsyncMock(spec=AsyncSession)


@pytest.mark.asyncio
async def test_create_user(session):
    user_data = {
        "username": "testuser",
        "hashed_password": "securepassword",
    }
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    user_in = UserCreate(**user_data)

    created_user = await create_user(session, user_in)

    assert isinstance(created_user, User)
    assert created_user.username == user_data["username"]
    assert created_user.hashed_password.decode("utf-8") == user_data["hashed_password"]
    session.add.assert_any_call(created_user)
    assert session.add.call_count == 1 + 6
    session.flush.assert_awaited_once()
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once_with(created_user)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, expected_user",
    [
        ("testuser", User(id=1, username="testuser", hashed_password="password")),
        ("unknown", None),
    ],
)
async def test_get_user_by_username(session, username, expected_user):
    mock_result = MagicMock(spec=Result)
    mock_result.scalars.return_value.first.return_value = expected_user
    session.execute.return_value = mock_result

    result = await get_user_by_username(session, username=username)

    assert result == expected_user
    session.execute.assert_called_once()
