from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session
from config.db import get_db
from config.redis import get_redis
from apps.metrics.models import Event
from apps.campaigns.models import Campaign
from apps.metrics.service import publish_event
from sqlalchemy import func
import asyncio
import json

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.post("/impressions/{campaign_id}")
async def track_impression(campaign_id: int, db: Session = Depends(get_db)):
    event = Event(campaign_id=campaign_id, tenant_id=1, type="impression")
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"status": "ok", "event_id": event.id}


@router.post("/clicks/{campaign_id}")
async def track_click(campaign_id: int, db: Session = Depends(get_db)):
    event = Event(campaign_id=campaign_id, tenant_id=1, type="click")
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"status": "ok", "event_id": event.id}


@router.get("/summary/{campaign_id}")
async def metrics_summary(campaign_id: int, db: Session = Depends(get_db)):
    summary = (
        db.query(Event.type, func.count(Event.id))
        .filter(Event.campaign_id == campaign_id)
        .group_by(Event.type)
        .all()
    )
    return {k: v for k, v in summary}


@router.websocket("/realtime/metrics/{campaign_id}")
async def websocket_metrics(ws: WebSocket, campaign_id: int, redis: Redis = Depends(get_redis)):
    await ws.accept()
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"campaign:{campaign_id}:metrics")

    try:
        while True:
            message = await pubsub.get_message(timeout=1.0)
            if message and message["type"] == "message":
                data = json.loads(message["data"])
                await ws.send_json(data)
            await asyncio.sleep(0.1)
    except Exception:
        await ws.close()
    finally:
        await pubsub.unsubscribe(f"campaign:{campaign_id}:metrics")
        await pubsub.close()



@router.post("/impressions/{campaign_id}")
async def track_impression(campaign_id: int, db: Session = Depends(get_db)):
    event = Event(campaign_id=campaign_id, tenant_id=1, type="impression")
    db.add(event)
    db.commit()
    db.refresh(event)
    # Publish to Redis
    asyncio.create_task(publish_event(campaign_id, "impression"))
    return {"status": "ok", "event_id": event.id}

@router.post("/clicks/{campaign_id}")
async def track_click(campaign_id: int, db: Session = Depends(get_db)):
    event = Event(campaign_id=campaign_id, tenant_id=1, type="click")
    db.add(event)
    db.commit()
    db.refresh(event)
    # Publish to Redis
    asyncio.create_task(publish_event(campaign_id, "click"))
    return {"status": "ok", "event_id": event.id}
