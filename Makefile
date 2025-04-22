.EXPORT_ALL_VARIABLES:
COMPOSE_FILE ?= docker-compose.yml
COMPOSE_TEST_FILE ?= docker-compose.test.yml

.PHONY: up
up:
	docker-compose --file $(COMPOSE_FILE) up --remove-orphans --force-recreate -d
	docker-compose ps

.PHONY: down
down:
	docker-compose --file $(COMPOSE_FILE) down

.PHONY: upgrade
upgrade:
	docker-compose exec book_management_db_migration alembic -c app/migrations/alembic.ini upgrade heads

.PHONY: downgrade
downgrade:
	docker-compose exec book_management_db_migration alembic -c app/migrations/alembic.ini downgrade -1

.PHONY: migrate
migrate:
	docker-compose exec --user root book_management_db_migration alembic -c app/migrations/alembic.ini revision --autogenerate -m "$(m)"

lint:
	pre-commit run --all-files
