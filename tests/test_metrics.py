"""
Tests para los endpoints de métricas.

Prueba el endpoint de métricas agregadas por campaña con tenant isolation.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_campaign_metrics():
    """
    Test: Obtener métricas agregadas de una campaña con tenant isolation.

    Verifica que el endpoint retorna impressions, clicks y CTR correctamente.
    """
    # ARRANGE: Mock DB session con datos de ejemplo
    impressions_count = 100
    clicks_count = 10

    class DummyQuery:
        def __init__(self, count):
            self._count = count
            self._filters = {}

        def filter_by(self, **kwargs):
            self._filters = kwargs
            # Retornar impressions o clicks según el filtro
            if kwargs.get("type") == "impression":
                self._count = impressions_count
            elif kwargs.get("type") == "click":
                self._count = clicks_count
            return self

        def count(self):
            return self._count

    class DummyDB:
        def query(self, model):
            return DummyQuery(0)

    # ACT: Override dependency y hacer request
    def fake_get_db():
        yield DummyDB()

    app.dependency_overrides[app.dependency_overrides.get] = fake_get_db

    from config.db import get_db
    app.dependency_overrides[get_db] = fake_get_db

    headers = {"X-Tenant-ID": "1"}
    response = client.get("/metrics/campaigns/1/metrics", headers=headers)

    # ASSERT: Verificar respuesta
    assert response.status_code == 200
    data = response.json()
    assert "impressions" in data
    assert "clicks" in data
    assert "ctr" in data
    assert data["impressions"] == impressions_count
    assert data["clicks"] == clicks_count
    assert data["ctr"] == clicks_count / impressions_count

    # Cleanup
    app.dependency_overrides.clear()
