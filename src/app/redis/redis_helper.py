import redis.asyncio as redis

from app.config import settings


class RedisHelper:
    def __init__(
        self,
        host: str = settings.redis.host,
        port: int = settings.redis.port,
        db: int = settings.redis.db,
        decode_responses: bool = settings.redis.decode_responses,
    ):
        self.redis_client = redis.Redis(
            host=host, port=port, db=db, decode_responses=decode_responses
        )


redis_helper = RedisHelper()
