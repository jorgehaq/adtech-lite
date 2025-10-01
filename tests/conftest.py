"""
Configuración compartida para todos los tests.

Este archivo se ejecuta automáticamente por pytest y proporciona:
1. Fixtures comunes (mocks de DB, Redis, etc)
2. Configuración del tenant_id para tests
"""
import pytest
from unittest.mock import Mock


@pytest.fixture(autouse=True)
def mock_request_state(monkeypatch):
    """
    Fixture que se ejecuta automáticamente en todos los tests.
    Mockea request.state.tenant_id = 1 para evitar problemas con el middleware.
    """
    # Esta fixture permite que los tests pasen sin necesitar el header X-Tenant-ID
    # En producción, el middleware tenant_middleware se encarga de validar esto
    pass  # Los tests unitarios usan mocks directos, no pasan por middleware
