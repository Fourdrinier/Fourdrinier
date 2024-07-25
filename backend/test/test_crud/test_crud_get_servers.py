"""
test_crud_get_servers.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Tests for the CRUD operations for servers

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from httpx import AsyncClient

import backend.app.db.crud as crud
from backend.app.db.models import Server, User


@pytest.mark.asyncio
async def test_crud_get_servers_000_nominal_no_servers(
    client: AsyncClient, test_db: AsyncSession
) -> None:
    """
    Test 000 - Nominal
    Conditions: No servers in the database
    Result: []
    """
    # Ensure that an empty list is returned
    assert await crud.get_servers(test_db) == []


@pytest.mark.asyncio
async def test_crud_get_servers_001_nominal_one_server(
    client: AsyncClient, test_db: AsyncSession, seed_user: User
) -> None:
    """
    Test 001 - Nominal
    Conditions: One server in the database
    Result: [<server>]
    """
    # Create a server
    seed_server = Server(
        id="abcdefgh",
        name="Test Server",
        game_version="1.17.1",
        loader="paper",
        owner=seed_user,
    )
    test_db.add(seed_server)
    await test_db.commit()
    await test_db.refresh(seed_server)

    # Ensure that the server is returned
    assert await crud.get_servers(test_db) == [seed_server]
