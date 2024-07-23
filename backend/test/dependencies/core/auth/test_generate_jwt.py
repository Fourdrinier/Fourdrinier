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
from datetime import datetime

from backend.app.dependencies.core.jwt.get_secret_key import get_secret_key
from backend.app.dependencies.core.auth.generate_jwt import generate_jwt


@pytest.mark.asyncio
async def test_generate_jwt_000_nominal(
    test_jwt_secret_key: None, test_jwt_expiration_time: str
):
    """
    Test 000 - Nominal
    Conditions: Username provided
    Result: JWT returned
    """
    # Generate the JWT
    token: str = generate_jwt(username="username")
    assert token

    # Ensure that the payload was inserted correctly
    payload: str = jwt.decode(token, get_secret_key(), algorithms=["HS256"])  # type: ignore
    username: str = payload.get("sub")
    assert username == "username"
