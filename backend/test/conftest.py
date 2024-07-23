"""
conftest.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Set up fixtures for testing

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os
import shutil
import secrets
from typing import AsyncGenerator
import pytest_asyncio
from _pytest.monkeypatch import MonkeyPatch

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from httpx import AsyncClient
from httpx import ASGITransport

from backend.app.db.models import Base, User
from backend.app.db.session import get_db
from backend.app.app import app

from backend.app.dependencies.registration_token.registration_token import (
    generate_registration_token,
)
from backend.app.dependencies.core.auth.generate_jwt import generate_jwt
from backend.app.dependencies.core.auth.get_password_hash import get_password_hash

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
TEST_STORAGE = "/tmp/fourdrinier"

test_secret_key: str = secrets.token_hex(32)


@pytest_asyncio.fixture(scope="function", autouse=True)  # type: ignore
async def test_storage() -> AsyncGenerator[str, None]:
    """
    Create a temporary storage directory for use in testing
    """
    try:
        os.makedirs(TEST_STORAGE, exist_ok=True)
        yield TEST_STORAGE
    finally:
        shutil.rmtree(TEST_STORAGE)


@pytest_asyncio.fixture(scope="session", autouse=True)  # type: ignore
async def test_db_engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create a database engine for use in testing
    """
    engine: AsyncEngine = create_async_engine(TEST_DB_URL)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def test_db(test_db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a database session for use in testing
    """
    # Create the tables
    async with test_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create and yield a session
    AsyncSessionMaker = async_sessionmaker(bind=test_db_engine)
    async with AsyncSessionMaker() as async_session:
        yield async_session

    # Clean up
    async with test_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client for use in testing
    """

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"  # type: ignore
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def test_reg_token(
    monkeypatch: MonkeyPatch, test_storage: str
) -> AsyncGenerator[str, None]:
    """
    Create a registration token file for use in testing
    """
    registration_token_file: str = os.path.join(test_storage, "registration_token")
    monkeypatch.setenv("REGISTRATION_TOKEN_FILE", registration_token_file)
    yield generate_registration_token()
    os.remove(registration_token_file)


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def seed_user(test_db: AsyncSession) -> AsyncGenerator[User, None]:
    user = User(
        username="test-user",
        hashed_password=await get_password_hash("password"),
        refresh_token=None,
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    yield user


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def seed_user2(test_db: AsyncSession) -> AsyncGenerator[User, None]:
    user = User(
        username="test-user2",
        hashed_password=await get_password_hash("password"),
        refresh_token=None,
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    yield user


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def seed_superuser(test_db: AsyncSession) -> AsyncGenerator[User, None]:
    user = User(
        username="admin",
        hashed_password=await get_password_hash("password"),
        refresh_token=None,
        is_superuser=True,
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    yield user


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def test_jwt_secret_key(monkeypatch: MonkeyPatch) -> None:
    secret_key: str = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", secret_key)


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def test_jwt_expiration_time(
    monkeypatch: MonkeyPatch,
) -> AsyncGenerator[str, None]:
    expiration_time = "3600"
    monkeypatch.setenv("JWT_EXPIRATION_TIME", expiration_time)
    yield expiration_time


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def test_jwt(
    seed_user: User, test_jwt_secret_key: str, test_jwt_expiration_time: str
) -> AsyncGenerator[str, None]:
    jwt: str = generate_jwt(str(seed_user.username))
    yield jwt


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def test_jwt_user2(
    seed_user2: User, test_jwt_secret_key: str, test_jwt_expiration_time: str
) -> AsyncGenerator[str, None]:
    jwt: str = generate_jwt(str(seed_user2.username))
    yield jwt


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def test_jwt_superuser(
    seed_superuser: User, test_jwt_secret_key: str, test_jwt_expiration_time: str
) -> AsyncGenerator[str, None]:
    jwt = generate_jwt(str(seed_superuser.username))
    yield jwt
