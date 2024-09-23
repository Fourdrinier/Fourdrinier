# Makefile

# Use shell command interpreter
SHELL := /bin/bash 

# Docker Compose configurations
PROD_CONFIG = -f docker-compose.yml
TEST_CONFIG = -f docker-compose.test.yml

# Default tag for alembic revision
ALEMBIC_TAG = "new_revision"

# Define targets
.PHONY: prepare_cache build build_test test

# Perform unit tests with isolated database
prepare_cache:
	mkdir -p $(PWD)/.pytest_cache
	chmod -R 777 $(PWD)/.pytest_cache

prepare_logs:
	mkdir -p $(PWD)/logs
	chmod 777 $(PWD)/logs

build:
	docker-compose $(PROD_CONFIG) build backend

build_test:
	docker-compose $(TEST_CONFIG) build backend

cleanup:
	- docker-compose $(PROD_CONFIG) down -v
	- docker-compose $(TEST_CONFIG) down -v

revision:
	- docker-compose $(TEST_CONFIG) down -v
	docker-compose $(TEST_CONFIG) build backend
	docker-compose $(TEST_CONFIG) run --rm --volume $(PWD)/backend/app/alembic/versions:/fourdrinier/backend/app/alembic/versions backend ls
	docker-compose $(TEST_CONFIG) run --rm --volume $(PWD)/backend/app/alembic/versions:/fourdrinier/backend/app/alembic/versions --entrypoint /fourdrinier/backend/scripts/generate_revision.sh backend $(ALEMBIC_TAG)
	- docker-compose $(TEST_CONFIG) down -v

migrate_test:
	docker-compose $(TEST_CONFIG) run --rm --volume $(PWD)/backend/app/alembic/versions:/fourdrinier/backend/app/alembic/versions backend python -m alembic upgrade head
	docker-compose $(TEST_CONFIG) down

test: prepare_cache prepare_logs build_test migrate_test
	- docker-compose $(TEST_CONFIG) run --rm --volume $(PWD)/backend/app/alembic/versions:/fourdrinier/backend/app/alembic/versions --volume $(PWD)/.pytest_cache:/fourdrinier/.pytest_cache --volume $(PWD)/logs:/fourdrinier/logs backend python -m pytest
	docker-compose $(TEST_CONFIG) down -v

test-verbose: prepare_cache prepare_logs build_test migrate_test
	- docker-compose $(TEST_CONFIG) run --rm --volume $(PWD)/backend/app/alembic/versions:/fourdrinier/backend/app/alembic/versions --volume $(PWD)/.pytest_cache:/fourdrinier/.pytest_cache --volume $(PWD)/logs:/fourdrinier/logs backend python -m pytest -vvv
	docker-compose $(TEST_CONFIG) down -v


