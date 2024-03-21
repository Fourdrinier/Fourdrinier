"""
conftest.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Set up fixtures for testing

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.models import Base
from app.db.session import get_db
from app.app import app

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_db_engine():
    """
    Create a database engine for use in testing
    """
    engine = create_async_engine(TEST_DB_URL)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_db(test_db_engine):
    """
    Create a database session for use in testing
    """
    # Create the tables
    async with test_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create and yield a session
    async_session = sessionmaker(
        test_db_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session

    # Clean up
    async with test_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(monkeypatch, test_db):
    """
    Create a test client for use in testing
    """

    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client