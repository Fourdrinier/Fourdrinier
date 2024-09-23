#!/bin/bash

python -m alembic upgrade head
python -m alembic revision --autogenerate -m "$1"