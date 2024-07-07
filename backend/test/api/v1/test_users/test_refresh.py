"""
test_refresh.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality of POST /users/refresh

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import secrets
import pytest

from fastapi.testclient import TestClient

from backend.app.dependencies.core.auth.generate_jwt import generate_jwt


@pytest.mark.asyncio
async def test_refresh_000_nominal(
    client,
    test_db,
    seed_user,
    test_jwt_secret_key,
    test_jwt_expiration_time,
):
    """
    Test 000 - Nominal
    Conditions: Valid username and refresh token given
    Result: HTTP 201 - New JWT and refresh token returned
    """
    # Generate the JWT
    jwt = generate_jwt(username=seed_user.username)

    # Create a initial refresh token
    initial_refresh_token = secrets.token_hex(32)
    seed_user.refresh_token = initial_refresh_token
    await test_db.commit()
    await test_db.refresh(seed_user)

    # Refresh the JWT
    query_params = {
        "refresh_token": seed_user.refresh_token,
        "client_id": seed_user.username,
    }
    response = await client.post("/api/v1/users/refresh", params=query_params)
    assert response.status_code == 200
    response_data = response.json()

    # Ensure that the new refresh token is different from the initial token
    await test_db.refresh(seed_user)
    assert seed_user.refresh_token != initial_refresh_token
    assert seed_user.refresh_token == response_data["refresh_token"]


@pytest.mark.asyncio
async def test_refresh_001_anomalous_no_token(monkeypatch, client, test_db, seed_user):
    """
    Test 001 - Anomalous
    Conditions: Valid username given, no refresh token given
    Result: HTTP 422 - Pydantic error
    """
    # Set the secret key
    test_secret_key = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", test_secret_key)

    # Create a initial refresh token
    initial_refresh_token = secrets.token_hex(32)
    seed_user.refresh_token = initial_refresh_token
    await test_db.commit()
    await test_db.refresh(seed_user)

    # Make the request
    query_params = {"client_id": seed_user.username}
    response = await client.post("/api/v1/users/refresh", params=query_params)

    # Ensure that the request failed
    assert response.status_code == 422
    response_data = response.json()
    assert response_data["detail"] == [
        {
            "type": "missing",
            "loc": ["query", "refresh_token"],
            "msg": "Field required",
            "input": None,
            "url": "https://errors.pydantic.dev/2.6/v/missing",
        }
    ]

    # Ensure that the refresh token did not change
    await test_db.refresh(seed_user)
    assert seed_user.refresh_token == initial_refresh_token


@pytest.mark.asyncio
async def test_refresh_002_anomalous_no_username(
    monkeypatch, client, test_db, seed_user
):
    """
    Test 002 - Anomalous
    Conditions: No username given, valid refresh token given
    Result: HTTP 422 - Pydantic error
    """
    # Set the secret key
    test_secret_key = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", test_secret_key)

    # Create a initial refresh token
    initial_refresh_token = secrets.token_hex(32)
    seed_user.refresh_token = initial_refresh_token
    await test_db.commit()
    await test_db.refresh(seed_user)

    # Make the request
    query_params = {"refresh_token": seed_user.refresh_token}
    response = await client.post("/api/v1/users/refresh", params=query_params)

    # Ensure that the request failed
    assert response.status_code == 422
    response_data = response.json()
    assert response_data["detail"] == [
        {
            "type": "missing",
            "loc": ["query", "client_id"],
            "msg": "Field required",
            "input": None,
            "url": "https://errors.pydantic.dev/2.6/v/missing",
        }
    ]

    # Ensure that the refresh token did not change
    await test_db.refresh(seed_user)
    assert seed_user.refresh_token == initial_refresh_token


@pytest.mark.asyncio
async def test_refresh_003_anomalous_invalid_username(
    monkeypatch, client, test_db, seed_user
):
    """
    Test 003 - Anomalous
    Conditions: Invalid username given
    Result: HTTP 401 - "The provided credentials were incorrect"
    """
    # Set the secret key
    test_secret_key = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", test_secret_key)

    # Create a initial refresh token
    initial_refresh_token = secrets.token_hex(32)
    seed_user.refresh_token = initial_refresh_token
    await test_db.commit()
    await test_db.refresh(seed_user)

    # Make the request
    query_params = {
        "client_id": "invalid-user",
        "refresh_token": seed_user.refresh_token,
    }
    response = await client.post("/api/v1/users/refresh", params=query_params)

    # Ensure that the request failed
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "The provided credentials were incorrect"

    # Ensure that the refresh token did not change
    await test_db.refresh(seed_user)
    assert seed_user.refresh_token == initial_refresh_token


@pytest.mark.asyncio
async def test_refresh_004_anomalous_invalid_token(
    monkeypatch, client, test_db, seed_user
):
    """
    Test 004 - Anomalous
    Conditions: Invalid refresh token given
    Result: HTTP 401 - "The provided credentials were incorrect"
    """
    # Set the secret key
    test_secret_key = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", test_secret_key)

    # Create a initial refresh token
    initial_refresh_token = secrets.token_hex(32)
    seed_user.refresh_token = initial_refresh_token
    await test_db.commit()
    await test_db.refresh(seed_user)

    # Make the request
    query_params = {"client_id": seed_user.username, "refresh_token": "invalid-token"}
    response = await client.post("/api/v1/users/refresh", params=query_params)

    # Ensure that the request failed
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "The provided credentials were incorrect"

    # Ensure that the refresh token did not change
    await test_db.refresh(seed_user)
    assert seed_user.refresh_token == initial_refresh_token


@pytest.mark.asyncio
async def test_refresh_005_anomalous_invalid_username_and_token(
    monkeypatch, client, test_db, seed_user
):
    """
    Test 005 - Anomalous
    Conditions: Invalid username and refresh token given
    Result: HTTP 401 - "The provided credentials were incorrect"
    """
    # Set the secret key
    test_secret_key = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", test_secret_key)

    # Create a initial refresh token
    initial_refresh_token = secrets.token_hex(32)
    seed_user.refresh_token = initial_refresh_token
    await test_db.commit()
    await test_db.refresh(seed_user)

    # Make the request
    query_params = {"client_id": "invalid-user", "refresh_token": "invalid-token"}
    response = await client.post("/api/v1/users/refresh", params=query_params)

    # Ensure that the request failed
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "The provided credentials were incorrect"

    # Ensure that the refresh token did not change
    await test_db.refresh(seed_user)
    assert seed_user.refresh_token == initial_refresh_token
