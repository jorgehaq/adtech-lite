from fastapi import FastAPI

app = FastAPI(title="Adtech Lite", version="0.1.0")

@app.get("/health")
def healthcheck():
    return {"status": "ok"}