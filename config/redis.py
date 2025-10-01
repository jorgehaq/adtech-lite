import os
import aioredis
from functools import lru_cache

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

@lru_cache
def get_redis_url() -> str:
    return REDIS_URL

async def get_redis():
    return await aioredis.from_url(get_redis_url(), decode_responses=True)
