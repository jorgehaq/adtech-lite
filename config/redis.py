# config/redis.py
import os
from redis.asyncio import Redis, ConnectionPool

# Pool de conexiones
pool = ConnectionPool.from_url(
    os.getenv("REDIS_URL", "redis://redis:6379/0"),
    decode_responses=True,
    max_connections=10,
)

# Cliente Redis compartido
redis_client = Redis(connection_pool=pool)

# Dependencia para FastAPI
async def get_redis() -> Redis:
    try:
        await redis_client.ping()
        return redis_client
    except Exception as e:
        raise RuntimeError(f"Redis connection failed: {e}")

