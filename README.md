# Adtech Lite

Adtech Lite is a lightweight AdTech analytics API built with **FastAPI**, **SQLAlchemy**, **MySQL**, and **Redis**.
It demonstrates **multi-tenant event tracking**, **real-time metrics with WebSockets**, and **database migrations with Alembic**.

## Features
- Track impressions and clicks per campaign
- Multi-tenant support using `X-Tenant-ID` header
- Real-time event broadcasting via Redis Pub/Sub and WebSockets
- Aggregated metrics endpoint with summary statistics
- Healthcheck endpoint validating DB and Redis connectivity
- Dockerized setup for local, dev, and production (GCP Cloud Run ready)

## Tech Stack
- **FastAPI** - Modern async web framework
- **SQLAlchemy + Alembic** - ORM and database migrations
- **MySQL** - Relational database
- **Redis** - Pub/Sub for real-time events
- **Docker & Docker Compose** - Containerization
- **Poetry** - Dependency management
- **Pytest** - Testing with 63% coverage

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+
- Poetry

### Run Locally
```bash
# Build and start containers
make docker-dev-build

# Apply database migrations
make alembic-upgrade

# Run tests
make test
```

### Available Commands
```bash
# Docker
make docker-dev-build        # Build and start all services
make docker-down-rm-volume   # Stop and remove volumes
make docker-test-models      # Test model imports in container

# Alembic Migrations
make alembic-revision MSG="your message"  # Create new migration
make alembic-upgrade                      # Apply pending migrations
make reset-db                             # Reset database (dangerous!)

# Testing
make test                    # Run all tests with coverage
```

## API Endpoints

### Metrics
- `POST /metrics/impressions/{campaign_id}` - Track impression (requires `X-Tenant-ID` header)
- `POST /metrics/clicks/{campaign_id}` - Track click (requires `X-Tenant-ID` header)
- `GET /metrics/summary/{campaign_id}` - Get aggregated metrics
- `WS /metrics/realtime/metrics/{campaign_id}` - Real-time metrics via WebSocket

### Health
- `GET /health` - Health check (DB + Redis status)

## Testing

### Unit Tests with Pytest
- **Mocked dependencies** for fast, isolated tests
- **AAA pattern** (Arrange-Act-Assert) for clarity
- **63% code coverage** across core modules

```bash
make test  # Run all tests with coverage report
```

### Test Structure
```
tests/
├── conftest.py          # Shared fixtures
├── test_redis.py        # Redis connection test
├── test_health.py       # Health endpoint test
└── test_websocket.py    # WebSocket + Redis Pub/Sub test
```

## Environment Configuration

### `.env.local`
Used by Docker Compose for container services (MySQL, Redis)

### `.env.host`
Used locally for Alembic migrations and tests
```bash
DATABASE_URL=mysql+pymysql://devuser:devpass@127.0.0.1:3306/adtech_lite_db?charset=utf8mb4
REDIS_URL=redis://127.0.0.1:6379/0
```

## Architecture

### Multi-Tenant Middleware
All API requests (except `/health`, `/docs`) require `X-Tenant-ID` header for tenant isolation.

### Real-Time Events
- Events are tracked in MySQL
- Redis Pub/Sub broadcasts events to WebSocket clients
- Clients receive real-time updates via WebSocket connection

## License
MIT