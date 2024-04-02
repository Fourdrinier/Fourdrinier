"""
test_register_user.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Tests for the users endpoint

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest
from fastapi.testclient import TestClient

from app.dependencies.registration_token.registration_token import (
    generate_registration_token,
)
from app.db.models import User


@pytest.mark.asyncio
async def test_register_user_000_nominal_superuser(
    monkeypatch, client, test_db, test_reg_token
):
    """
    Test 000 - Nominal
    Conditions: Registration token provided
    Result: HTTP 201: Superuser created
    """
    monkeypatch.setenv("REGISTRATION_TOKEN", test_reg_token)
    response = client.post(
        "/api/v1/users/register/",
        json={
            "username": "test_user",
            "password": "test_password",
            "is_superuser": True,
            "registration_token": test_reg_token,
        },
    )
    assert response.status_code == 201

    user = await test_db.get(User, "test_user")
    assert user is not None
    assert user.username == "test_user"
    assert user.is_superuser
