"""
config.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Configuration settings for the FastAPI application.

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os


PROJECT_NAME = "fourdrinier"
DB_URL: str = os.getenv("DB_URL", "sqlite+aiosqlite:///./db-data/fourdrinier.db")
DOCKER_HOST: str | None = os.getenv("DOCKER_HOST", "/var/run/docker.sock")
