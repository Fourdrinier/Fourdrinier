#!/bin/bash

echo "Generating revision with message: $1"
python -m alembic upgrade head
python -m alembic revision --autogenerate -m "$1"