"""
test_list_servers.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Tests for the servers endpoint

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest
from fastapi.testclient import TestClient

from app.db.models import Server


@pytest.mark.asyncio
async def test_list_servers_000_nominal_no_servers(client):
    """
    Test 000 - Nominal
    Conditions: No servers in the database
    Result: HTTP 200 - Empty list returned
    """
    response = client.get("/api/v1/servers/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_servers_001_nominal_one_server(client, test_db):
    """
    Test 001 - Nominal
    Conditions: One server in the database
    Result: HTTP 200 - One server object returned
    """
    # Add a server to the database
    server = Server(id="abcdefgh", name="Test Server")
    test_db.add(server)
    await test_db.commit()

    # Make a request to the server endpoint
    response = client.get("/api/v1/servers/")
    assert response.status_code == 200
    assert response.json() == [{"id": "abcdefgh", "name": "Test Server"}]
