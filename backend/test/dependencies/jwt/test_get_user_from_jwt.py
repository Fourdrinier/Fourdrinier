"""
test_get_user_from_jwt.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality of get_user_from_jwt()

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest

import os
import secrets

from app.app import app
from app.dependencies.jwt.generate_jwt import generate_jwt
from app.dependencies.jwt.get_user_from_jwt import get_user_from_jwt

from app.db.session import get_db


@pytest.mark.asyncio
async def test_get_user_from_jwt_000_nominal(
    monkeypatch, seed_user, test_db, test_jwt_secret_key
):
    """
    Test 000 - Nominal
    Conditions: JWT is valid
    Result: User object returned
    """
    # Generate a valid JWT
    username = seed_user.username
    jwt = generate_jwt(username)

    # Ensure that the user object is returned\
    user = await get_user_from_jwt(jwt, test_db)
    assert user
    assert user.username == username
