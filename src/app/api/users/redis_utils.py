from datetime import timedelta

from app.redis.redis_helper import redis_helper


async def increment_failed_attempts(username: str) -> int:
    """Tracks failed login attempts with automatic 5-min counter expiration."""
    key = f"failed_attempts:{username}"
    attempts = await redis_helper.redis_client.incr(key)
    if attempts == 1:
        await redis_helper.redis_client.expire(key, 300)
    return attempts


async def lock_account(username: str) -> None:
    """Temporarily locks user account after repeated failed login attempts."""
    await redis_helper.redis_client.set(
        f"locked:{username}", "true", ex=timedelta(minutes=5)
    )


async def is_account_locked(username: str) -> bool:
    """Checks if account is currently locked."""
    return (
        await redis_helper.redis_client.get(f"locked:{username}") is not None
    )
