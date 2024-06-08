# Use the official Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /backend

# Install Poetry for dependency management
RUN pip install poetry

# Install dependencies using Poetry
COPY pyproject.toml poetry.lock* /backend/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy the alembic.ini file to the container
COPY alembic.ini /backend/alembic.ini

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Copy the rest of your application's code
COPY ./app /backend/app

# Copy in the configuration file
COPY ./config.json /backend/config.json

# Start the FastAPI app
CMD python -m alembic upgrade head && python -m uvicorn app.app:app --host 0.0.0.0 --port 8000