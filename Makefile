PROJECT_NAME=adtech-lite
REGION=us-central1
GCP_PROJECT_ID?=your-gcp-project-id
IMAGE=gcr.io/$(GCP_PROJECT_ID)/$(PROJECT_NAME):latest
IMAGE_LOCAL=$(PROJECT_NAME):latest

# Docker status
docker-status-origin:
	curl -4 -I --max-time 10 https://registry-1.docker.io/v2/

docker-status:
	docker compose -f docker/docker-compose.local.yml ps

docker-prune:
	docker system prune -f

dockre-rm-old-images:
	docker image prune -af

docker-rm-huerfanos-volumes:
	docker volume prune -f 


docker-push:
	docker push $(IMAGE)

docker-volume-rm:
	docker volume rm adtech-lite_mysql_data





# Run DOCKER
docker-dev:
	docker compose -f docker/docker-compose.local.yml up

docker-dev-build:
	docker compose -f docker/docker-compose.local.yml up --build

docker-dev-not-cache:
	docker compose -f docker/docker-compose.local.yml build --no-cache && \
	docker compose -f docker/docker-compose.local.yml up

dev-check-environment-local:
	docker exec -it adtech-lite-api env | grep -E "DATABASE_URL|REDIS_URL|ENVIRONMENT"

docker-down-rm-volume:
	docker compose -f docker/docker-compose.local.yml down -v

docker-down:
	docker compose -f docker/docker-compose.local.yml down






# MySQL
dev-mysql-check-root:
	docker exec -it adtech-lite-mysql mysql -u root -p

dev-mysql-check-devuser:
	set -a && . ./.env.local && docker exec -it adtech-lite-mysql mysql -u $$MYSQL_USER -p$$MYSQL_PASSWORD adtech_lite_db

mysql-status:
	docker exec adtech-lite-mysql mysqladmin -u root -p status

mysql-logs:
	docker logs adtech-lite-mysql





# INSTALL
poetry-install:
	poetry install

# Exporta requirements.txt desde Poetry
poetry-generate-requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

# Build de Docker asegurando requirements.txt actualizado
docker-build: poetry-generate-requirements
	docker build -t $(IMAGE_LOCAL) -f docker/Dockerfile .




# ALEMBIC LOCAL
alembic-init:
	poetry run alembic init alembic

alembic-migrate:
	set -a && . ./.env.host && set +a && \
	poetry run alembic revision --autogenerate -m "init tables" && \
	poetry run alembic upgrade head

alembic-rm-previous-versions:
	rm -rf alembic/versions/*
	


# PYTEST
test:
	set -a && . ./.env.host && pytest -v --asyncio-mode=auto --cov=apps --cov=config --cov-report=term-missing


# TEST DOCKER MODELOS
docker-test-models:
	docker exec adtech-lite-api python -c "from apps.campaigns.models import Campaign; from apps.metrics.models import Event; print(Campaign, Event)"


docker-test-db:
	docker exec adtech-lite-api python -c "import os; from apps.campaigns.models import Campaign; from apps.metrics.models import Event; print('DB=', os.getenv('DATABASE_URL')); print(Campaign, Event)"
	set -a && . ./.env.local && docker exec adtech-lite-mysql mysql -u $$MYSQL_USER -p$$MYSQL_PASSWORD adtech_lite_db -e "SHOW TABLES;"




# INSTALL POETRY DEPENENCIES
poetry-mysql-8-criptography:
	poetry add cryptography && make poetry-generate-requirements






# GCP
gcp-deploy: build push
	gcloud run deploy $(PROJECT_NAME)-api \
		--image $(IMAGE) \
		--platform managed \
		--region $(REGION) \
		--allow-unauthenticated \
		--add-cloudsql-instances $(GCP_PROJECT_ID):$(REGION):$(PROJECT_NAME)-db \
		--set-env-vars DATABASE_URL=$$DATABASE_URL \
		--set-env-vars REDIS_URL=$$REDIS_URL