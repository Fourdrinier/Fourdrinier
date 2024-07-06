"""
test_register_superuser.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Tests for the users endpoint

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest
from fastapi.testclient import TestClient

from sqlalchemy import select

from backend.app.db.models import User


@pytest.mark.asyncio
async def test_register_superuser_000_nominal_superuser(
    monkeypatch, client, test_db, test_reg_token
):
    """
    Test 000 - Nominal
    Conditions: No users in database
    Result: HTTP 201: Superuser created
    """
    monkeypatch.setenv("REGISTRATION_TOKEN", test_reg_token)
    response = await client.post(
        "/api/v1/users/superuser/",
        json={
            "username": "test_user",
            "password": "test_password",
            "registration_token": test_reg_token,
        },
    )
    assert response.status_code == 201

    user = await test_db.get(User, "test_user")
    assert user is not None
    assert user.username == "test_user"
    assert user.is_superuser


@pytest.mark.asyncio
async def test_register_superuser_001_anomalous_superuser_present(
    monkeypatch, client, test_db, test_reg_token
):
    """
    Test 001 - Existing user
    Conditions: One superuser in database
    Result: HTTP 404: Superuser not created
    """
    # Create a superuser
    user = User(username="test_user1", hashed_password="abcdefg", is_superuser=True)
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)

    # Attempt to create a new superuser
    monkeypatch.setenv("REGISTRATION_TOKEN", test_reg_token)
    response = await client.post(
        "/api/v1/users/superuser/",
        json={
            "username": "test_user2",
            "password": "test_password",
            "registration_token": test_reg_token,
        },
    )

    # Check that the response is 404
    assert response.status_code == 404

    # Check that the user was not created
    user_response = await test_db.execute(select(User))
    users = user_response.scalars().all()
    assert len(users) == 1


@pytest.mark.asyncio
async def test_register_superuser_002_anomalous_no_registration_token(
    monkeypatch, client, test_db, test_reg_token
):
    """
    Test 002 - No registration token
    Conditions: No users in database
    Result: HTTP 400: Superuser not created
    """
    # Attempt to create a superuser without a registration token
    monkeypatch.setenv("REGISTRATION_TOKEN", test_reg_token)
    response = await client.post(
        "/api/v1/users/superuser/",
        json={"username": "test_user", "password": "test_password"},
    )

    # Check that the correct error message is returned
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Superuser registration requires a registration token"
    }

    # Check that the user was not created
    user_response = await test_db.execute(select(User))
    users = user_response.scalars().all()
    assert len(users) == 0


@pytest.mark.asyncio
async def test_register_superuser_003_anomalous_invalid_registration_token(
    monkeypatch, client, test_db, test_reg_token
):
    """
    Test 003 - Invalid registration token
    Conditions: Invalid token included in request to register superuser
    Result: HTTP 400: Invalid registration token
    """
    # Attempt to create a superuser with an invalid registration token
    monkeypatch.setenv("REGISTRATION_TOKEN", test_reg_token)
    response = await client.post(
        "/api/v1/users/superuser/",
        json={
            "username": "test_user",
            "password": "test_password",
            "registration_token": "invalid_token",
        },
    )

    # Check that the correct error message is returned
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid registration token"}

    # Check that the user was not created
    user_response = await test_db.execute(select(User))
    users = user_response.scalars().all()
    assert len(users) == 0
