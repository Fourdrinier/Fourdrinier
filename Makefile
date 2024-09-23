# Makefile

# Use shell command interpreter
SHELL := /bin/bash

# Docker configurations
PRODUCTION_CONFIG = --profile default

ALEMBIC_TAG ?= "initial revision"

# Define targets
.PHONY: build-backend run cleanup revision

# Build the backend
build-backend:
	@echo "Building the backend..."
	@docker compose $(PRODUCTION_CONFIG) build backend

# Run the application
run: build-backend
	@echo "Running the application..."
	@docker compose $(PRODUCTION_CONFIG) up

# Remove containers and volumes
cleanup:
	@echo "Cleaning up..."
	@docker compose $(PRODUCTION_CONFIG) down --volumes

revision: build-backend
	@echo "Creating a new revision..."
	@docker compose $(PRODUCTION_CONFIG) run --rm --volume $(PWD)/backend/fourdrinier/alembic/versions:/fd/backend/fourdrinier/alembic/versions --entrypoint /fd/backend/scripts/generate_revision.sh backend $(ALEMBIC_TAG)