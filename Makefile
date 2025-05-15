.PHONY: build-prod up-prod down-prod build-dev up-dev down-dev logs

# Production commands
build-prod:
	docker-compose -f docker-compose.prod.yml build

up-prod:
	docker-compose -f docker-compose.prod.yml up -d

down-prod:
	docker-compose -f docker-compose.prod.yml down

logs:
	docker-compose -f docker-compose.prod.yml logs -f

# Development commands
build-dev:
	docker-compose -f docker-compose.dev.yml build

up-dev:
	docker-compose -f docker-compose.dev.yml up -d

down-dev:
	docker-compose -f docker-compose.dev.yml down
