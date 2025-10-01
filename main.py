from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from config.db import get_db
from config.redis import redis_client

app = FastAPI(title="Adtech Lite", version="0.2.0")

# Healthcheck básico
@app.get("/health")
def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")  # test DB
        redis_client.ping()     # test Redis
        return {"status": "ok", "db": "connected", "redis": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}