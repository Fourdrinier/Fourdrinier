"""
test_get_secret_key.py

@Author: Ethan Brown - ethan@ewbrowntech.com

This file contains the tests for the get_secret_key function

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest
import os
import secrets
from backend.app.dependencies.jwt.get_secret_key import get_secret_key


@pytest.mark.asyncio
async def test_get_secret_key_000_nominal_secret_key(monkeypatch):
    """
    Test 000 - Nominal
    Conditions: Environment variable "JWT_SECRET_KEY" is set as a string
    Result: Secret key string returned
    """
    # Set the environment variable
    secret_key = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", secret_key)

    # Ensure that the secret key is returned
    assert get_secret_key() == secret_key


@pytest.mark.asyncio
async def test_get_secret_key_001_secret_key_var_not_set():
    """
    Test 001 - Anomalous
    Conditions: Environment variable "JWT_SECRET_KEY" is not set
    Result: EnvironmentError("The environment variable JWT_SECRET_KEY cannot be empty")
    """
    # Ensure that an exception is raised
    with pytest.raises(EnvironmentError) as e:
        get_secret_key()

    assert str(e.value) == "The environment variable JWT_SECRET_KEY cannot be empty"


@pytest.mark.asyncio
async def test_get_secret_key_002_anomalous_secret_key_var_empty(monkeypatch):
    """
    Test 002 - Anomalous
    Conditions: Environment variable "JWT_SECRET_KEY" is an empty string
    Result: EnvironmentError("The environment variable JWT_SECRET_KEY cannot be empty")
    """
    # Set the environment variable
    monkeypatch.setenv("JWT_SECRET_KEY", "")

    # Ensure that the correct exception is raised
    with pytest.raises(EnvironmentError) as e:
        secret_key = get_secret_key()
    assert str(e.value) == "The environment variable JWT_SECRET_KEY cannot be empty"


@pytest.mark.asyncio
async def test_get_secret_key_003_anomalous_secret_key_too_short(monkeypatch):
    """
    Test 003 - Anomalous
    Conditions: Environment variable "SECRET_KEY" is a string that is < 256 bits (64 characters) long
    Result: ValueError("Secret key must be at least 256 bits (64 hexadecimal characters) long")
    """
    # Set the environment variable
    secret_key = secrets.token_hex(31)
    monkeypatch.setenv("JWT_SECRET_KEY", secret_key)

    # Ensure that the correct exception is raised
    with pytest.raises(ValueError) as e:
        get_secret_key()
    assert (
        str(e.value)
        == "The environment variable JWT_SECRET_KEY must be at least 256 bits (64 hexadecimal characters) long"
    )
