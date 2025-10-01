"""
Unit tests para WebSocket de métricas en tiempo real.

Usamos mocks porque:
1. Los unit tests deben ser rápidos e independientes de servicios externos
2. Queremos probar nuestra lógica de negocio, no Redis ni WebSocket
3. Los tests de integración (contra Docker) van en tests/integration/
"""
import pytest
import json
from unittest.mock import AsyncMock, patch
from fastapi import WebSocket
from apps.metrics.endpoints import websocket_metrics


@pytest.mark.asyncio
@patch('apps.metrics.endpoints.get_redis')
async def test_websocket_receives_redis_messages(mock_get_redis):
    """
    Test: Verificar que los mensajes de Redis se envían correctamente via WebSocket

    Escenario:
    1. Un cliente se conecta al WebSocket
    2. Redis publica un mensaje de "impression"
    3. El WebSocket debe recibir y reenviar ese mensaje al cliente
    """
    # ARRANGE: Configurar mocks de Redis
    mock_redis = AsyncMock()
    mock_pubsub = AsyncMock()

    # Simular que Redis devuelve un mensaje de tipo "impression"
    redis_message = {
        "type": "message",
        "data": json.dumps({"type": "impression", "campaign_id": 1})
    }
    mock_pubsub.get_message = AsyncMock(return_value=redis_message)
    mock_pubsub.subscribe = AsyncMock(return_value=None)
    mock_pubsub.unsubscribe = AsyncMock(return_value=None)
    mock_pubsub.close = AsyncMock(return_value=None)

    # pubsub() debe devolver directamente el mock (no como coroutine)
    mock_redis.pubsub = lambda: mock_pubsub
    mock_get_redis.return_value = mock_redis

    # ARRANGE: Configurar mock de WebSocket
    mock_ws = AsyncMock(spec=WebSocket)
    mock_ws.accept = AsyncMock()
    mock_ws.send_json = AsyncMock()

    # ACT: Ejecutar el endpoint (limitado a una iteración para el test)
    import asyncio
    task = asyncio.create_task(websocket_metrics(mock_ws, campaign_id=1, redis=mock_redis))
    await asyncio.sleep(0.1)  # Dar tiempo para procesar un mensaje
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass  # Esperado al cancelar

    # ASSERT: Verificar que se ejecutó el flujo correcto
    mock_ws.accept.assert_called_once()  # Acepta la conexión
    mock_pubsub.subscribe.assert_called_once_with("campaign:1:metrics")  # Se suscribe al canal

    # Verificar que se envió el mensaje al cliente
    assert mock_ws.send_json.called
    sent_data = mock_ws.send_json.call_args_list[0][0][0]
    assert sent_data["type"] in ["impression", "heartbeat"]
