"""
test_get_jwt_expiration.py

@Author: Ethan Brown - ethan@ewbrowntech.com

This file contains tests for get_jwt_expiration_time()

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest
from backend.app.dependencies.core.jwt.get_jwt_expiration import get_jwt_expiration_time


@pytest.mark.asyncio
async def test_get_jwt_expiration_time_000_nominal_expiration_time(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Test 000 - Nominal
    Conditions: Environment variable "JWT_EXPIRATION_TIME"is set to 1 (minutes)
    Result: Integer `1` returned
    """
    # Set the environment variable
    monkeypatch.setenv("JWT_EXPIRATION_TIME", "1")

    # Ensure that the expiration time is returned
    assert get_jwt_expiration_time() == 1


@pytest.mark.asyncio
async def test_get_jwt_expiration_time_001_anomalous_var_not_set() -> None:
    """
    Test 001 - Anomalous
    Conditions: Environment variable "JWT_EXPIRATION_TIME" is not set
    Result: EnvironmentError("The environment variable
                            JWT_EXPIRATION_TIME cannot be empty")
    """
    # Ensure that an exception is raised
    with pytest.raises(EnvironmentError) as e:
        get_jwt_expiration_time()

    assert (
        str(e.value) == "The environment variable JWT_EXPIRATION_TIME cannot be empty"
    )


@pytest.mark.asyncio
async def test_get_jwt_expiration_time_002_anomalous_var_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Test 002 - Anomalous
    Conditions: Environment variable "JWT_EXPIRATION_TIME" is an empty string
    Result: EnvironmentError("The environment variable
                            JWT_EXPIRATION_TIME cannot be empty")
    """
    # Set the environment variable
    monkeypatch.setenv("JWT_EXPIRATION_TIME", "")

    # Ensure that the correct exception is raised
    with pytest.raises(EnvironmentError) as e:
        get_jwt_expiration_time()
    assert (
        str(e.value) == "The environment variable JWT_EXPIRATION_TIME cannot be empty"
    )


@pytest.mark.asyncio
async def test_get_jwt_expiration_time_003_anomalous_not_digit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Test 003 - Anomalous
    Conditions: Environment variable "JWT_EXPIRATION_TIME" = "not_an_integer"
    Result: ValueError("The environment variable
                        JWT_EXPIRATION_TIME must be an integer")
    """
    # Set the environment variable
    monkeypatch.setenv("JWT_EXPIRATION_TIME", "not_an_integer")

    # Ensure that the correct exception is raised
    with pytest.raises(ValueError) as e:
        get_jwt_expiration_time()
    assert (
        str(e.value)
        == "The environment variable JWT_EXPIRATION_TIME must be an integer"
    )


@pytest.mark.asyncio
async def test_get_jwt_expiration_time_004_anomalous_non_integer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Test 004 - Anomalous
    Conditions: Environment variable "JWT_EXPIRATION_TIME" = "1.5"
    Result: ValueError("The environment variable
                        JWT_EXPIRATION_TIME must be an integer")
    """
    # Set the environment variable
    monkeypatch.setenv("JWT_EXPIRATION_TIME", "1.5")

    # Ensure that the correct exception is raised
    with pytest.raises(ValueError) as e:
        get_jwt_expiration_time()
    assert (
        str(e.value)
        == "The environment variable JWT_EXPIRATION_TIME must be an integer"
    )


@pytest.mark.asyncio
async def test_get_jwt_expiration_time_005_anomalous_less_than_one(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Test 005 - Anomalous
    Conditions: Environment variable "JWT_EXPIRATION_TIME" = "0"
    Result: ValueError("The environment variable JWT_EXPIRATION_TIME
                        must be >= 1 (in minutes)")
    """
    # Set the environment variable
    monkeypatch.setenv("JWT_EXPIRATION_TIME", "0")

    # Ensure that the correct exception is raised
    with pytest.raises(ValueError) as e:
        get_jwt_expiration_time()
    assert (
        str(e.value)
        == "The environment variable JWT_EXPIRATION_TIME must be >= 1 (in minutes)"
    )
