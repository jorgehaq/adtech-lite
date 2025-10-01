import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_healthcheck_ok(monkeypatch):
    # Mock DB
    def fake_execute(query):
        return True

    # Mock Redis
    class FakeRedis:
        def ping(self):
            return True

    # Monkeypatch DB + Redis
    app.dependency_overrides = {}
    monkeypatch.setattr("config.db.get_db", lambda: type("FakeSession", (), {"execute": fake_execute})())
    monkeypatch.setattr("config.redis.redis_client", FakeRedis())

    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["db"] == "connected"
    assert data["redis"] == "connected"
