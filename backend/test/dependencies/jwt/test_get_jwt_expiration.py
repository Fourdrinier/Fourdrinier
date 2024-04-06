"""
test_get_jwt_expiration.py

@Author: Ethan Brown - ethan@ewbrowntech.com

This file contains tests for get_jwt_expiration_time()

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest
from app.dependencies.jwt.get_jwt_expiration import get_jwt_expiration_time


@pytest.mark.asyncio
async def test_get_jwt_expiration_time_000_nominal_expiration_time(monkeypatch):
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
async def test_get_jwt_expiration_time_001_anomalous_var_not_set():
    """
    Test 001 - Anomalous
    Conditions: Environment variable "JWT_EXPIRATION_TIME" is not set
    Result: EnvironmentError("The environment variable JWT_EXPIRATION_TIME cannot be empty")
    """
    # Ensure that an exception is raised
    with pytest.raises(EnvironmentError) as e:
        get_jwt_expiration_time()

    assert (
        str(e.value) == "The environment variable JWT_EXPIRATION_TIME cannot be empty"
    )
