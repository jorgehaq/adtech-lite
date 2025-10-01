from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from config.db import get_db
from config.redis import redis_client
from config.logging import init_logging
from apps.metrics.endpoints import router as metrics_router
from apps.campaigns.endpoints import router as campaigns_router
from config.middleware.tenant import tenant_middleware
from config.middleware.request_id import request_id_middleware
from prometheus_fastapi_instrumentator import Instrumentator

init_logging()


app = FastAPI(title="Adtech Lite", version="0.2.0")

app.middleware("http")(tenant_middleware)
app.middleware("http")(request_id_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metrics_router)
app.include_router(campaigns_router)


# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "Adtech Lite API",
        "version": "0.2.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "campaigns": "/campaigns/",
            "metrics": "/metrics/"
        }
    }

# Healthcheck básico
@app.get("/health")
async def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))  # test DB
        await redis_client.ping()     # test Redis
        return {"status": "ok", "db": "connected", "redis": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}


Instrumentator().instrument(app).expose(app)