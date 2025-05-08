import pytest
from unittest.mock import AsyncMock
from datetime import timedelta
from app.api.users import redis_utils


@pytest.fixture
def mock_redis():
    return AsyncMock()


@pytest.fixture(autouse=True)
def setup_redis_mock(mock_redis):
    redis_utils.redis_helper.redis_client = mock_redis


@pytest.mark.parametrize(
    "attempts, ttl_called",
    [
        (1, True),
        (2, False),
        (5, False),
    ],
)
@pytest.mark.asyncio
async def test_increment_failed_attempts(mock_redis, attempts, ttl_called):
    username = "test_user"
    mock_redis.incr.return_value = attempts

    result = await redis_utils.increment_failed_attempts(username)

    assert result == attempts
    mock_redis.incr.assert_awaited_once_with(f"failed_attempts:{username}")

    if ttl_called:
        mock_redis.expire.assert_awaited_once_with(f"failed_attempts:{username}", 300)
    else:
        mock_redis.expire.assert_not_awaited()


@pytest.mark.asyncio
async def test_lock_account(mock_redis):
    username = "locked_user"

    await redis_utils.lock_account(username)

    mock_redis.set.assert_awaited_once_with(
        f"locked:{username}", "true", ex=timedelta(minutes=5)
    )


@pytest.mark.parametrize(
    "redis_return, expected",
    [
        ("true", True),
        (None, False),
    ],
)
@pytest.mark.asyncio
async def test_is_account_locked(mock_redis, redis_return, expected):
    username = "test_user"
    mock_redis.get.return_value = redis_return

    result = await redis_utils.is_account_locked(username)

    assert result == expected
    mock_redis.get.assert_awaited_once_with(f"locked:{username}")
