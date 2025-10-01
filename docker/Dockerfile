# Stage 1: build
FROM python:3.12-slim AS builder

WORKDIR /code

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copiar archivos de dependencias
COPY pyproject.toml poetry.lock* ./

# Exportar requirements.txt desde poetry
RUN poetry self add poetry-plugin-export && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes

# Instalar dependencias en un virtualenv temporal
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: runtime
FROM python:3.12-slim

WORKDIR /code

# Copiar dependencias del builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar el proyecto
COPY . .

# Puerto configurable
ENV PORT=8070
ENV WORKERS=4
# Por defecto, usamos uvicorn para desarrollo
ENV CMD="uvicorn main:app --host 0.0.0.0 --port $PORT"

# Ejecutar comando (puede sobreescribirse en Cloud Run o docker-compose)
CMD sh -c "$CMD"
