"""
test_list_servers.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Tests for the servers endpoint

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest

from httpx import AsyncClient, Response
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.models import Server, User


@pytest.mark.asyncio
async def test_list_servers_000_nominal_no_servers(client: AsyncClient) -> None:
    """
    Test 000 - Nominal
    Conditions: No servers in the database
    Result: HTTP 200 - Empty list returned
    """
    response: Response = await client.get("/api/v1/servers/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_servers_001_nominal_one_server(
    client: AsyncClient, test_db: AsyncSession, seed_user: User
) -> None:
    """
    Test 001 - Nominal
    Conditions: One server in the database
    Result: HTTP 200 - One server object returned
    """
    # Add a server to the database
    server = Server(
        id="abcdefgh",
        name="Test Server",
        loader="paper",
        game_version="1.17.1",
        owner=seed_user,
    )
    test_db.add(server)
    await test_db.commit()

    # Make a request to the server endpoint
    response: Response = await client.get("/api/v1/servers/")
    assert response.status_code == 200
    servers: Any = response.json()
    assert len(servers) == 1
    server: Any = servers[0]
    assert server["id"] == "abcdefgh"
    assert server["name"] == "Test Server"
    assert server["loader"] == "paper"
    assert server["game_version"] == "1.17.1"
