"""
session.py

@Author: Ethan Brown

Database session management for the Fourdrinier project

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import DeclarativeBase


# Database connection URL
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres"


# Create a base class for models
class Base(DeclarativeBase):
    pass


# Create the SQLAlchemy async session factory
async_engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine
)


# Dependency to get a database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            raise
