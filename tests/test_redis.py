import pytest
from unittest.mock import AsyncMock, patch
from config.redis import get_redis

@pytest.mark.asyncio
@patch('config.redis.redis_client')
async def test_redis_ping(mock_redis):
    mock_redis.ping = AsyncMock(return_value=True)
    redis = await get_redis()
    pong = await redis.ping()
    assert pong is True
