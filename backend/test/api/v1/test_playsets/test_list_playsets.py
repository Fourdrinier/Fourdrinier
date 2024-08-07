"""
test_list_playsets.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Tests for the GET /playsets

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from typing import Tuple, Any
import pytest

from httpx import AsyncClient, Response

from sqlalchemy.orm import selectinload
from sqlalchemy import Select, select
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.models import User, Playset


@pytest.mark.asyncio
async def test_list_playsets_000_nominal_no_playsets(
    client: AsyncClient, test_jwt_superuser: str
) -> None:
    """
    Test 000 - Nominal
    Conditions: No playsets in the database
    Result: HTTP 200 - Empty list returned
    """
    # Make a request to the playsets endpoint
    response: Response = await client.get(
        "/api/v1/playsets/", headers={"Authorization": f"Bearer {test_jwt_superuser}"}
    )

    # Ensure the correct response is returned
    assert response.status_code == 200
    playsets: Any = response.json()
    assert playsets == []


@pytest.mark.asyncio
async def test_list_playsets_001_nominal_no_playsets_available(
    client: AsyncClient, test_db: AsyncSession, test_jwt: str, seed_user2: User
) -> None:
    """
    Test 001 - Nominal
    Conditions: User test-user is not a superuser,
                user test-user2 has one private playset
    Result: HTTP 200 - Empty list returned
    """
    # Eagerly load in test-user2's playsets
    stmt: Select[Tuple[User]] = (
        select(User)
        .options(selectinload(User.playsets))
        .filter_by(username=seed_user2.username)
    )
    result: Result[Tuple[User]] = await test_db.execute(stmt)
    seed_user2 = result.scalar_one()

    # Add a playset to the user
    playset = Playset(id="abcdefgh", name="Test Playset", is_private=True)
    seed_user2.playsets.append(playset)
    await test_db.commit()

    # Make a request to the playsets endpoint as test-user
    response: Response = await client.get(
        "/api/v1/playsets/", headers={"Authorization": f"Bearer {test_jwt}"}
    )

    # Ensure the correct response is returned
    assert response.status_code == 200
    playsets: Any = response.json()
    assert playsets == []


@pytest.mark.asyncio
async def test_list_playsets_002_nominal_admin_views_private(
    client: AsyncClient, test_db: AsyncSession, seed_user: User, test_jwt_superuser: str
) -> None:
    """
    Test 002 - Nominal
    Conditions: Request sent by superuser, test-user has one private playset
    Result: HTTP 200 - [<test-user playset>]
    """
    # Eagerly load in test-user's playsets
    await test_db.refresh(seed_user)
    stmt: Select[Tuple[User]] = (
        select(User)
        .options(selectinload(User.playsets))
        .filter_by(username=seed_user.username)
    )
    result: Result[Tuple[User]] = await test_db.execute(stmt)
    seed_user: User | None = result.scalar_one()

    # Add a playset to the user
    playset = Playset(id="abcdefgh", name="Test Playset", is_private=True)
    seed_user.playsets.append(playset)
    await test_db.commit()

    # Make a request to the playsets endpoint as test-user
    response: Response = await client.get(
        "/api/v1/playsets/", headers={"Authorization": f"Bearer {test_jwt_superuser}"}
    )

    # Ensure the correct response is returned
    assert response.status_code == 200
    playsets: list[Any] = response.json()
    assert len(playsets) == 1
    playset: Any = playsets[0]
    assert playset["id"] == "abcdefgh"
    assert playset["name"] == "Test Playset"
    assert playset["is_private"] is True


@pytest.mark.asyncio
async def test_list_playsets_003_nominal_user1_views_user2_public(
    client: AsyncClient,
    test_db: AsyncSession,
    seed_user: User,
    seed_user2: User,
    test_jwt: str,
) -> None:
    """
    Test 003 - Nominal
    Conditions: Request sent by test-user1, test-user1 has one private playset,
                test-user2 has one public playset
    Result:HTTP 200 - [<test-user playset>, <test-user2 playset>]
    """
    # Eagerly load in test-user1's playsets
    await test_db.refresh(seed_user)
    stmt: Select[Tuple[User]] = (
        select(User)
        .options(selectinload(User.playsets))
        .filter_by(username=seed_user.username)
    )
    result: Result[Tuple[User]] = await test_db.execute(stmt)
    seed_user: User | None = result.scalar_one()

    # Add a private playset to test-user1
    playset: Playset = Playset(id="abcdefgh", name="Test Playset", is_private=True)
    seed_user.playsets.append(playset)
    await test_db.commit()

    # Eagery load in test-user2's playsets
    await test_db.refresh(seed_user2)
    stmt: Select[Tuple[User]] = (
        select(User)
        .options(selectinload(User.playsets))
        .filter_by(username=seed_user2.username)
    )
    result: Result[Tuple[User]] = await test_db.execute(stmt)
    seed_user2: User | None = result.scalar_one()

    # Add a public playset to test-user2
    playset: Playset = Playset(id="ijklmnop", name="Test Playset 2", is_private=False)
    seed_user2.playsets.append(playset)
    await test_db.commit()

    # Make a request to the playsets endpoint as test-user1
    response: Response = await client.get(
        "/api/v1/playsets/", headers={"Authorization": f"Bearer {test_jwt}"}
    )

    # Ensure the correct response is returned
    assert response.status_code == 200
    playsets: list[Any] = response.json()
    assert len(playsets) == 2
    ids: list[str] = [playset["id"] for playset in playsets]
    assert "abcdefgh" in ids
    assert "ijklmnop" in ids
