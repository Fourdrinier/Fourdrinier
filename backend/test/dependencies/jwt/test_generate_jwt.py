"""
test_generate_jwt.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality of generate_jwt()

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest
import jwt
import secrets

from app.dependencies.jwt.get_secret_key import get_secret_key
from app.dependencies.jwt.generate_jwt import generate_jwt

@pytest.mark.asyncio
async def test_generate_jwt_000_nominal(monkeypatch):
    """
    Test 000 - Nominal
    Conditions: Username provided
    Result: JWT returned
    """
    # Set the secret key environment variable
    secret_key = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", secret_key)

    # Set the expiration time environment variable
    monkeypatch.setenv("JWT_EXPIRATION_TIME", "1")

    # Generate the JWT
    token = generate_jwt(username="username")
    assert token

    # Ensure that the payload was inserted correctly
    payload = jwt.decode(token, get_secret_key(), algorithms=["HS256"])
    username: str = payload.get("username")
    assert username == "username"
    
@pytest.mark.asyncio
async def test_generate_jwt_001_anomalous_no_username(monkeypatch):
    """
    Test 001 - Anomalous
    Conditions: username = None
    Result: ValueError('username' must be of type <class 'str'>, not <class 'NoneType'>)
    """
    # Set the secret key environment variable
    secret_key = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", secret_key)

    # Set the expiration time environment variable
    monkeypatch.setenv("JWT_EXPIRATION_TIME", "1")

    # Ensure that an exception is raised
    with pytest.raises(ValueError) as e:
        jwt = generate_jwt(username=None)
    assert str(e.value) == "'username' must be of type <class 'str'>, not <class 'NoneType'>"


@pytest.mark.asyncio
async def test_generate_jwt_002_anomalous_username_is_not_string(monkeypatch):
    """
    Test 002 - Anomalous
    Conditions: username = 1
    Result: ValueError('username' must be of type <class 'str'>, not <class 'int'>)
    """
    # Set the secret key environment variable
    secret_key = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", secret_key)

    # Set the expiration time environment variable
    monkeypatch.setenv("JWT_EXPIRATION_TIME", "1")

    # Ensure that an exception is raised
    with pytest.raises(ValueError) as e:
        jwt = generate_jwt(username=1)
    assert str(e.value) == "'username' must be of type <class 'str'>, not <class 'int'>"