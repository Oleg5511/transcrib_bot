from redis.asyncio import Redis
from redis.asyncio.client import Pipeline

redis: Redis | None = None


async def get_redis() -> Redis:
    """Возвращает синглтон Redis"""
    return redis
