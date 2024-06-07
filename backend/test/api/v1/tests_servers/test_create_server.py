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
        json={"name": "Test Server", "loader": "paper", "game_version": "1.20.0"},
    )

    # Ensure the correct response is returned
    assert response.status_code == 201
    server = response.json()
    assert server["name"] == "Test Server"
    assert server["loader"] == "paper"
    assert server["game_version"] == "1.20.0"

    # Ensure the server was added to the database
    result = await test_db.execute(select(Server))
    servers = result.scalars().all()
    assert len(servers) == 1
    server = servers[0]
    assert server.name == "Test Server"
    assert server.loader == "paper"
    assert server.game_version == "1.20.0"


@pytest.mark.asyncio
async def test_create_server_001_anomalous_unauthorized(client, test_db):
    """
    Test 001 - Anomalous
    Conditions: Unauthorized request
    Result: HTTP 401 - Unauthorized
    """
    # Make a request to the server endpoint
    response = client.post(
        "/api/v1/servers/",
        json={"name": "Test Server", "loader": "paper", "game_version": "1.20"},
    )

    # Ensure the correct response is returned
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    # Ensure the server was not added to the database
    result = await test_db.execute(select(Server))
    servers = result.scalars().all()
    assert len(servers) == 0


@pytest.mark.asyncio
async def test_create_server_002_anomalous_invalid_loader(client, test_db, test_jwt):
    """
    Test 002 - Anomalous
    Conditions: loader = "invalid"
    Result: HTTP 400 - "Invalid loader"
    """
    # Make a request to the server endpoint
    response = client.post(
        "/api/v1/servers/",
        headers={"Authorization": f"Bearer {test_jwt}"},
        json={"name": "Test Server", "loader": "invalid", "game_version": "1.20.0"},
    )

    # Ensure the correct response is returned
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid loader"

    # Ensure the server was not added to the database
    result = await test_db.execute(select(Server))
    servers = result.scalars().all()
    assert len(servers) == 0


@pytest.mark.asyncio
async def test_create_server_003_anomalous_invalid_game_version(
    client, test_db, test_jwt
):
    """
    Test 003 - Anomalous
    Conditions: game_version = "invalid"
    Result: HTTP 400 - Validation error
    """
    # Make a request to the server endpoint
    response = client.post(
        "/api/v1/servers/",
        headers={"Authorization": f"Bearer {test_jwt}"},
        json={"name": "Test Server", "loader": "paper", "game_version": "invalid"},
    )

    # Ensure the correct response is returned
    assert response.status_code == 422
    detail = response.json()["detail"]
    print(detail[0]["msg"])
    assert detail[0]["msg"] == "String should match pattern '^\\d+\\.\\d+\\.\\d+$'"

    # Ensure the server was not added to the database
    result = await test_db.execute(select(Server))
    servers = result.scalars().all()
    assert len(servers) == 0


@pytest.mark.asyncio
async def test_create_server_004_anomalous_unsupported_game_version(
    client, test_db, test_jwt
):
    """
    Test 004 - Anomalous
    Conditions: game_version = "1.16.5"
    Result: HTTP 400 - "Unsupported game version"
    """
    # Make a request to the server endpoint
    response = client.post(
        "/api/v1/servers/",
        headers={"Authorization": f"Bearer {test_jwt}"},
        json={"name": "Test Server", "loader": "paper", "game_version": "2.0.0"},
    )

    # Ensure the correct response is returned
    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported game version"

    # Ensure the server was not added to the database
    result = await test_db.execute(select(Server))
    servers = result.scalars().all()
    assert len(servers) == 0
