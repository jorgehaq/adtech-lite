from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from config.db import get_db
from config.redis import redis_client
from apps.metrics.endpoints import router as metrics_router

app = FastAPI(title="Adtech Lite", version="0.2.0")

app.include_router(metrics_router)

# Healthcheck básico
@app.get("/health")
def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")  # test DB
        redis_client.ping()     # test Redis
        return {"status": "ok", "db": "connected", "redis": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}