import json
from config.redis import get_redis

async def publish_event(campaign_id: int, event_type: str):
    redis = await get_redis()
    payload = {"type": event_type, "campaign_id": campaign_id}
    await redis.publish(f"campaign:{campaign_id}:metrics", json.dumps(payload))

