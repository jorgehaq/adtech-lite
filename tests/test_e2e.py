"""
Integration E2E test - Connects to real Docker services (MySQL + Redis).

Requirements:
- Docker containers running (make docker-dev)
- Database migrations applied (make alembic-upgrade)
- Services accessible at localhost:8070
"""
import pytest
import httpx
import os

BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8070")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_e2e_flow():
    """
    End-to-end integration test for the complete flow:
    1. Create campaign
    2. Track impressions and clicks
    3. Verify aggregated metrics

    Uses real DB and Redis connections via Docker.
    """
    headers = {"X-Tenant-ID": "1", "Content-Type": "application/json"}

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        # Step 1: Create campaign
        response = await client.post(
            "/campaigns/",
            headers=headers,
            json={"name": "E2E Test Campaign"}
        )
        assert response.status_code == 200
        campaign_id = response.json()["id"]

        # Step 2: Track 3 impressions
        for _ in range(3):
            response = await client.post(
                f"/metrics/impressions/{campaign_id}",
                headers=headers
            )
            assert response.status_code == 200

        # Step 3: Track 1 click
        response = await client.post(
            f"/metrics/clicks/{campaign_id}",
            headers=headers
        )
        assert response.status_code == 200

        # Step 4: Get aggregated metrics
        response = await client.get(
            f"/metrics/campaigns/{campaign_id}/metrics",
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()

        # Step 5: Verify metrics
        assert data["impressions"] == 3
        assert data["clicks"] == 1
        assert abs(data["ctr"] - (1/3)) < 0.01
