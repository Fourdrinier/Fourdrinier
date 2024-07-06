# Use the official Python base image
FROM python:3.11-slim

# Create a non-root user and group
RUN adduser --system --no-create-home nonroot

# Set the working directory in the container
WORKDIR /fourdrinier

# Install Poetry for dependency management
RUN pip install poetry

# Install dependencies using Poetry
COPY pyproject.toml poetry.lock* /fourdrinier/backend/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy the alembic.ini file to the container
COPY alembic.ini /fourdrinier/backend/alembic.ini

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Copy the rest of your application's code
COPY ./app /fourdrinier/backend/app

# Copy in the configuration file
COPY ./config.json /fourdrinier/backend/config.json

# Create the directory and change ownership
RUN mkdir -p /var/lib/fourdrinier && \
    chown -R nonroot /var/lib/fourdrinier

# Switch to the non-root user
USER nonroot

# Create the registration token file
RUN touch /var/lib/fourdrinier/registration_token

# Start the FastAPI app
CMD python -m alembic upgrade head && python -m uvicorn backend.app.app:app --host 0.0.0.0 --port 8000