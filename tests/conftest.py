"""
Pytest configuration and fixtures.

This file runs before all tests and sets up mocks for external services.
"""
import sys
from unittest.mock import AsyncMock, MagicMock
import pytest


# Mock Redis module BEFORE any test imports it
mock_redis_client = AsyncMock()
mock_redis_client.ping = AsyncMock(return_value=True)

mock_pool = MagicMock()

mock_redis_module = MagicMock()
mock_redis_module.redis_client = mock_redis_client
mock_redis_module.pool = mock_pool
mock_redis_module.get_redis = AsyncMock(return_value=mock_redis_client)

sys.modules['config.redis'] = mock_redis_module


@pytest.fixture
def mock_request_state(monkeypatch):
    """
    Mock request.state.tenant_id for tests that don't go through middleware.
    """
    pass
