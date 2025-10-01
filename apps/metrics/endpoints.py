from fastapi import APIRouter, Depends, WebSocket, Request
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from config.db import get_db
from config.redis import get_redis
from apps.metrics.models import Event
from sqlalchemy import func
import asyncio
import json

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.post("/impressions/{campaign_id}")
async def track_impression(
    campaign_id: int,
    db: Session = Depends(get_db),
    request: Request = None
):
    tenant_id = request.state.tenant_id
    event = Event(
        campaign_id=campaign_id,
        tenant_id=tenant_id,
        type="impression"
    )
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
            msg = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if msg and msg["type"] == "message":
                data = json.loads(msg["data"])
                await ws.send_json(data)
            # Heartbeat cada 30s
            await ws.send_json({"type": "heartbeat"})
            await asyncio.sleep(30)
    except Exception:
        await ws.close()
    finally:
        await pubsub.unsubscribe(f"campaign:{campaign_id}:metrics")
        await pubsub.close()

