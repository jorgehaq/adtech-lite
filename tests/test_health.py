"""
Health endpoint test.

Tests the /health endpoint with mocked database and Redis.
Redis is mocked globally in conftest.py.
"""
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app
from config.db import get_db


def test_healthcheck_ok():
    """Test health endpoint returns ok with mocked services."""
    # Mock DB session
    mock_session = MagicMock()
    mock_session.execute.return_value = True

    def fake_get_db():
        yield mock_session

    app.dependency_overrides[get_db] = fake_get_db

    client = TestClient(app)
    response = client.get("/health")

    # Cleanup
    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["db"] == "connected"
    assert data["redis"] == "connected"
