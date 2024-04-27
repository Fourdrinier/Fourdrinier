"""
test_create_server.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Tests for creating a server

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db.models import Server


@pytest.mark.asyncio
async def test_create_server_000_nominal(client, test_db, test_jwt):
    """
    Test 000 - Nominal
    Conditions: Valid server object
    Result: HTTP 201 - Server object returned
    """
    # Make a request to the server endpoint
    response = client.post(
        "/api/v1/servers/",
        headers={"Authorization": f"Bearer {test_jwt}"},
        json={"name": "Test Server", "loader": "paper", "game_version": "1.17.1"},
    )

    # Ensure the correct response is returned
    assert response.status_code == 201
    server = response.json()
    assert server["name"] == "Test Server"
    assert server["loader"] == "paper"
    assert server["game_version"] == "1.17.1"

    # Ensure the server was added to the database
    result = await test_db.execute(select(Server))
    servers = result.scalars().all()
    assert len(servers) == 1
    server = servers[0]
    assert server.name == "Test Server"
    assert server.loader == "paper"
    assert server.game_version == "1.17.1"
