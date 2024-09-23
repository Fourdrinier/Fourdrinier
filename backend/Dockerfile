####################################################################################################
# Base Image
####################################################################################################
FROM ubuntu:22.04 AS base

# Update base image packages
RUN apt-get update && apt-get install -y ca-certificates && \
    apt-get update && apt-get upgrade -y

# Install Python & Curl
RUN apt-get install -y python3 python3-pip curl

# Install Poetry for dependency management
RUN python3 -m pip install poetry

# Define Poetry's environment variables
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VENV=/opt/poetry-venv
ENV PATH="${POETRY_VENV}/bin:${PATH}"

# Set the working directory
WORKDIR /fd

####################################################################################################
# Base Image Builder
####################################################################################################
FROM base AS builder

# Install root dependencies
COPY pyproject.toml poetry.lock /fd/
RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-dev

####################################################################################################
# Production Image
####################################################################################################
FROM base AS prod

# Copy the virtual environment from the builder stage
COPY --from=builder /fd/.venv ${POETRY_VENV}

# Copy the source code
COPY ./fourdrinier/alembic.ini /fd/alembic.ini
COPY ./fourdrinier /fd/backend/fourdrinier

# Copy in the scripts
COPY ./scripts /fd/backend/scripts

EXPOSE 8000

# Run the FastAPI server
CMD python3 -m uvicorn backend.fourdrinier.main:app --host 0.0.0.0 --port 8000