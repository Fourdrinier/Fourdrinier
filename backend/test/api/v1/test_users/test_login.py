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
    response = client.post(
        "/api/v1/users/login", json={"username": "test-user", "password": "password"}
    )
    assert response.status_code == 200
    response_data = response.json()

    # Refresh the seeded user to get the refresh token
    await test_db.refresh(seed_user)

    # Verify the JWT
    assert "jwt" in response_data
    token = response_data["jwt"]
    assert token is not None
    payload = jwt.decode(token, get_secret_key(), algorithms=["HS256"])
    username: str = payload.get("sub")
    assert username == "test-user"

    # Verify the refresh token
    assert "refresh_token" in response_data
    refresh_token = response_data["refresh_token"]
    assert refresh_token is not None
    assert refresh_token == seed_user.refresh_token


@pytest.mark.asyncio
async def test_login_001_no_username_provided(monkeypatch, client, test_db, seed_user):
    """
    Test 001 - Anomalous
    Conditions: Password provided, but username missing
    Result: HTTP 400 - {Pydantic error}
    """
    # Make the request
    response = client.post("/api/v1/users/login", json={"password": "password"})
    assert response.status_code == 422
    response_data = response.json()
    assert response_data == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "username"],
                "msg": "Field required",
                "input": {"password": "password"},
                "url": "https://errors.pydantic.dev/2.6/v/missing",
            }
        ]
    }
    assert seed_user.refresh_token is None

    # Verify that the user was not logged in
    user_response = await test_db.execute(
        select(User).filter_by(username=seed_user.username)
    )
    user = user_response.scalars().first()
    assert user is not None
    assert user.refresh_token is None


@pytest.mark.asyncio
async def test_login_002_anomalous_no_password_provided(
    monkeypatch, client, test_db, seed_user
):
    """
    Test 002 - Anomalous
    Conditions: Username provided, but password missing
    Result: HTTP 400 - {Pydantic error}
    """
    # Make the request
    response = client.post("/api/v1/users/login", json={"username": "test-user"})
    assert response.status_code == 422
    response_data = response.json()
    assert response_data == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "password"],
                "msg": "Field required",
                "input": {"username": "test-user"},
                "url": "https://errors.pydantic.dev/2.6/v/missing",
            }
        ]
    }
    assert seed_user.refresh_token is None

    # Verify that the user was not logged in
    user_response = await test_db.execute(
        select(User).filter_by(username=seed_user.username)
    )
    user = user_response.scalars().first()
    assert user is not None
    assert user.refresh_token is None


@pytest.mark.asyncio
async def test_login_003_anomalous_nonexistent_user(
    monkeypatch, client, test_db, seed_user
):
    """
    Test 003 - Anomalous
    Conditions: Username provided does not exist
    Result: HTTP 401 - "The provided credentials were incorrect"
    """
    # Make the request
    response = client.post(
        "/api/v1/users/login", json={"username": "test-user2", "password": "password"}
    )
    assert response.status_code == 401
    response_data = response.json()
    assert response_data == {"detail": "The provided credentials were incorrect"}
    assert seed_user.refresh_token is None

    # Verify that the user was not logged in
    user_response = await test_db.execute(
        select(User).filter_by(username=seed_user.username)
    )
    user = user_response.scalars().first()
    assert user is not None
    assert user.refresh_token is None


@pytest.mark.asyncio
async def test_login_004_anomalous_incorrect_password(
    monkeypatch, client, test_db, seed_user
):
    """
    Test 004 - Anomalous
    Conditions: Incorrect password provided
    Result: HTTP 401 - "The provided credentials were incorrect"
    """
    # Make the request
    response = client.post(
        "/api/v1/users/login", json={"username": "test-user", "password": "password2"}
    )
    assert response.status_code == 401
    response_data = response.json()
    assert response_data == {"detail": "The provided credentials were incorrect"}
    assert seed_user.refresh_token is None

    # Verify that the user was not logged in
    user_response = await test_db.execute(
        select(User).filter_by(username=seed_user.username)
    )
    user = user_response.scalars().first()
    assert user is not None
    assert user.refresh_token is None
