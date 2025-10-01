PROJECT_NAME=adtech-lite
REGION=us-central1
IMAGE=gcr.io/$(GCP_PROJECT_ID)/$(PROJECT_NAME):latest

# Docker status
docker-status-origin:
	curl -4 -I --max-time 10 https://registry-1.docker.io/v2/

docker-status:
	docker compose -f docker/docker-compose.local.yml ps

docker-prune:
	docker system prune -f

docker-build:
	docker build -t $(IMAGE) .

docker-push:
	docker push $(IMAGE)

docker-volume-rm:
	docker volume rm adtech-lite_mysql_data

docker-down-clear-volume:
	docker compose -f docker/docker-compose.local.yml down -v





# Run DOCKER
docker-dev:
	docker compose -f docker/docker-compose.local.yml up --build

docker-dev-not-cache:
	docker compose -f docker/docker-compose.local.yml up --build --no-cache

dev-check-environment-local:
	docker exec -it edtech-lite-api env | grep -E "DATABASE_URL|REDIS_URL|ENVIRONMENT"

docker-down:
	docker compose -f docker/docker-compose.local.yml down -v






# MySQL
dev-mysql-check-root:
	docker exec -it edtech-lite-mysql mysql -u root -proot

dev-mysql-check-devuser:
	docker exec -it edtech-lite-mysql mysql -u devuser -pdevpass adtech_lite_db

mysql-status:
	docker exec edtech-lite-mysql mysqladmin -u root -proot status

mysql-logs:
	docker logs edtech-lite-mysql





# INSTALL
poetry-generate-requirements:
	poetry export -f requirements.txt --output requirements.txt
	


# PYTEST
test:
	pytest -v --asyncio-mode=auto --cov=adtech --cov-report=term-missing



# ALEMBIC
migrate:
	alembic revision --autogenerate -m "new migration"
	alembic upgrade head



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