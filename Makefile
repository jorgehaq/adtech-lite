PROJECT_NAME=adtech-lite
REGION=us-central1
GCP_PROJECT_ID?=your-gcp-project-id
IMAGE=gcr.io/$(GCP_PROJECT_ID)/$(PROJECT_NAME):latest
IMAGE_LOCAL=$(PROJECT_NAME):latest

# Containers
API_CONTAINER=adtech-lite-api
MYSQL_CONTAINER=adtech-lite-mysql
REDIS_CONTAINER=adtech-lite-redis

# -------------------------------------------------------------------
# 🐳 Docker
# -------------------------------------------------------------------
docker-status-origin:
	curl -4 -I --max-time 10 https://registry-1.docker.io/v2/

docker-status:
	docker compose -f docker/docker-compose.local.yml ps

docker-prune:
	docker system prune -f

docker-rm-old-images:
	docker image prune -af

docker-rm-orphan-volumes:
	docker volume prune -f

docker-dev:
	docker compose -f docker/docker-compose.local.yml up

docker-dev-build:
	docker compose -f docker/docker-compose.local.yml up --build

docker-dev-no-cache:
	docker compose -f docker/docker-compose.local.yml build --no-cache && \
	docker compose -f docker/docker-compose.local.yml up

docker-down:
	docker compose -f docker/docker-compose.local.yml down

docker-down-rm-volume:
	docker compose -f docker/docker-compose.local.yml down -v

docker-info:
	docker ps -s

# -------------------------------------------------------------------
# 🗄️ MySQL
# -------------------------------------------------------------------
dev-mysql-root:
	docker exec -it $(MYSQL_CONTAINER) mysql -u root -p

dev-mysql-user:
	set -a && . ./.env.local && docker exec -it $(MYSQL_CONTAINER) \
	mysql -u $$MYSQL_USER -p$$MYSQL_PASSWORD adtech_lite_db

mysql-status:
	docker exec $(MYSQL_CONTAINER) mysqladmin -u root -p status

mysql-logs:
	docker logs $(MYSQL_CONTAINER)

# -------------------------------------------------------------------
# 📦 Poetry & Requirements
# -------------------------------------------------------------------
poetry-install:
	poetry install

poetry-generate-requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

docker-build: poetry-generate-requirements
	docker build -t $(IMAGE_LOCAL) -f docker/Dockerfile .

# -------------------------------------------------------------------
# 🔄 Alembic
# -------------------------------------------------------------------
alembic-init:
	poetry run alembic init alembic

alembic-revision:
	set -a && . ./.env.host && poetry run alembic revision --autogenerate -m "$(MSG)"

alembic-upgrade:
	set -a && . ./.env.host && poetry run alembic upgrade head

alembic-clean:
	rm -rf alembic/versions/*

reset-db:
	make docker-down-rm-volume
	make docker-dev-build
	make alembic-clean
	make alembic-upgrade

# -------------------------------------------------------------------
# ✅ Tests
# -------------------------------------------------------------------
test:
	set -a && . ./.env.host && pytest -v --asyncio-mode=auto --cov=apps --cov=config --cov-report=term-missing

docker-test-models:
	docker exec $(API_CONTAINER) python -c "from apps.campaigns.models import Campaign; from apps.metrics.models import Event; print(Campaign, Event)"

docker-test-db:
	docker exec $(API_CONTAINER) python -c "import os; from apps.campaigns.models import Campaign; from apps.metrics.models import Event; print('DB=', os.getenv('DATABASE_URL')); print(Campaign, Event)"
	set -a && . ./.env.local && docker exec -it $(MYSQL_CONTAINER) mysql -u $$MYSQL_USER -p$$MYSQL_PASSWORD adtech_lite_db -e "SHOW TABLES;"

# -------------------------------------------------------------------
# 🚀 GCP Deploy
# -------------------------------------------------------------------
gcp-deploy: docker-build docker-push
	gcloud run deploy $(PROJECT_NAME)-api \
		--image $(IMAGE) \
		--platform managed \
		--region $(REGION) \
		--allow-unauthenticated \
		--add-cloudsql-instances $(GCP_PROJECT_ID):$(REGION):$(PROJECT_NAME)-db \
		--set-env-vars DATABASE_URL=$$DATABASE_URL \
		--set-env-vars REDIS_URL=$$REDIS_URL
