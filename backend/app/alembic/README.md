Generic single-database configuration with an async dbapi.

    docker-compose run --rm -v $(pwd):/backend backend python -m alembic revision --autogenerate -m "Initial revision"