"""
test_login.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality of POST /users/login
"""

import pytest

import jwt
import secrets
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db.models import User

from app.dependencies.jwt.get_secret_key import get_secret_key

@pytest.mark.asyncio
async def test_login_000_nominal(monkeypatch, client, test_db, seed_user):
    """
    Test 000 - Nominal
    Conditions: Correct username and password provided
    Result: HTTP 200 - JWT and refresh token returned
    """
    test_secret_key = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", test_secret_key)

    # Make the request
    response = client.post("/api/v1/users/login", json={"username": "test-user", "password": "password"})
    assert response.status_code == 200
    response_data = response.json()
    
    # Refresh the seeded user to get the refresh token
    await test_db.refresh(seed_user)

    # Verify the JWT
    assert "jwt" in response_data
    token = response_data["jwt"]
    assert token is not None
    payload = jwt.decode(token, get_secret_key(), algorithms=["HS256"])
    username: str = payload.get("username")
    assert username == "test-user"

    # Verify the refresh token
    assert "refresh_token" in response_data
    refresh_token = response_data["refresh_token"]
    assert refresh_token is not None
    assert refresh_token == seed_user.refresh_token