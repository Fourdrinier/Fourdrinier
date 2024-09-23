# Makefile

# Use shell command interpreter
SHELL := /bin/bash

# Docker configurations
PRODUCTION_CONFIG = --profile default

# Define targets
.PHONY: build-backend run cleanup

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