# Stage 1: builder
FROM python:3.12-slim AS builder
WORKDIR /code

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock* ./
RUN poetry self add poetry-plugin-export && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: runtime
FROM python:3.12-slim
WORKDIR /code

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy only what you need
COPY apps/ ./apps
COPY config/ ./config
COPY main.py . 
COPY alembic ./alembic
COPY alembic.ini .

ENV PORT=8070
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8070"]
