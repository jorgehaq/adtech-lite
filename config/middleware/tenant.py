from fastapi import Request, HTTPException

# Rutas que no requieren tenant_id (health checks, docs, etc)
EXCLUDED_PATHS = {"/", "/health", "/docs", "/redoc", "/openapi.json"}

async def tenant_middleware(request: Request, call_next):
    # Bypass middleware para rutas excluidas
    if request.url.path in EXCLUDED_PATHS:
        response = await call_next(request)
        return response

    # Validar tenant_id para el resto de rutas
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID required")

    request.state.tenant_id = int(tenant_id)
    response = await call_next(request)
    return response
