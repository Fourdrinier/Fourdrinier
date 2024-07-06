# Makefile

# Use shell command interpreter
SHELL := /bin/bash 

# Docker Compose configurations
PROD_CONFIG = -f docker-compose.yml
TEST_CONFIG = -f docker-compose.test.yml

# Define targets
.PHONY: prepare_cache build build_test test

# Perform unit tests with isolated database
prepare_cache:
	mkdir -p $(PWD)/.pytest_cache
	chmod -R 777 $(PWD)/.pytest_cache

build:
	docker-compose $(PROD_CONFIG) build backend

build_test:
	docker-compose $(TEST_CONFIG) build backend

test: prepare_cache build_test
	- docker-compose $(TEST_CONFIG) run --rm --volume $(PWD)/backend/app/alembic/versions:/backend/app/alembic/versions --volume $(PWD)/.pytest_cache:/fourdrinier/.pytest_cache backend python -m pytest
	docker-compose $(TEST_CONFIG) down -v