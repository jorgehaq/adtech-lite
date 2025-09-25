PROJECT_NAME=adtech-lite
REGION=us-central1
IMAGE=gcr.io/$(GCP_PROJECT_ID)/$(PROJECT_NAME):latest

dev:
	docker compose -f docker/docker-compose.local.yml up --build

down:
	docker compose -f docker/docker-compose.local.yml down -v

test:
	pytest -v --asyncio-mode=auto --cov=adtech --cov-report=term-missing

migrate:
	alembic revision --autogenerate -m "new migration"
	alembic upgrade head

build:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

deploy: build push
	gcloud run deploy $(PROJECT_NAME)-api \
		--image $(IMAGE) \
		--platform managed \
		--region $(REGION) \
		--allow-unauthenticated \
		--add-cloudsql-instances $(GCP_PROJECT_ID):$(REGION):$(PROJECT_NAME)-db \
		--set-env-vars DATABASE_URL=$$DATABASE_URL \
		--set-env-vars REDIS_URL=$$REDIS_URL