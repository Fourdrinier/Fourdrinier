# Makefile

# Use shell command interpreter
SHELL := /bin/bash

# Docker Compose configurations
PROD_CONFIG = -f docker-compose.yml
TEST_CONFIG = -f docker-compose.test.yml

# Define targets
.PHONY: test

# Perform unit tests with isolated database
test:
	docker-compose $(TEST_CONFIG) build backend
	- docker-compose $(TEST_CONFIG) run --rm --volume $(PWD)/backend/app/alembic/versions:/backend/app/alembic/versions backend python -m pytest
	docker-compose $(TEST_CONFIG) down -v