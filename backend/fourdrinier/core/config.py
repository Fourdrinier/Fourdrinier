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

# Base URL for PostgreSQL database
POSTGRES_URL_BASE: str = (
    f"{os.getenv('POSTGRES_USER', 'postgres')}:{os.getenv('POSTGRES_PASSWORD', 'postgres')}"
    f"@{os.getenv('POSTGRES_HOST', 'postgres')}:{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB', 'fourdrinier')}"
)

# Database URLs
DATABASE_URL: str = f"postgresql://{POSTGRES_URL_BASE}"
ASYNC_DATABASE_URL: str = f"postgresql+asyncpg://{POSTGRES_URL_BASE}"
