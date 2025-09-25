FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry && poetry install --no-root --no-dev

COPY . /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8070"]