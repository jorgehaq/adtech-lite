import json
import asyncio
from config.redis import get_redis


async def publish_event(campaign_id: int, event_type: str):
    redis = await get_redis()
    payload = {"campaign_id": campaign_id, "event": event_type}
    await redis.publish(f"campaign:{campaign_id}:metrics", json.dumps(payload))
