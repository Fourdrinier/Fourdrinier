"""
test_get_user_from_jwt.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality of get_user_from_jwt()

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest

import base64
from datetime import datetime, timedelta, timezone
import json
import jwt
import secrets
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.dependencies.core.auth.generate_jwt import generate_jwt
from backend.app.dependencies.core.auth.get_user_from_jwt import get_user_from_jwt
from backend.app.dependencies.core.jwt.get_secret_key import get_secret_key

from backend.app.db.models import User


@pytest.mark.asyncio
async def test_get_user_from_jwt_000_nominal(
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 000 - Nominal
    Conditions: JWT is valid
    Result: User object returned
    """
    # Generate a valid JWT
    jwt: str = generate_jwt(str(seed_user.username))

    # Ensure that the user object is returned
    user: User = await get_user_from_jwt(jwt, test_db)
    assert user
    assert str(user.username) == seed_user.username


@pytest.mark.asyncio
async def test_get_user_from_jwt_001_bad_token_missing_header(
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 001 - Bad token - missing header
    Conditions: JWT is missing header
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    jwt: str = generate_jwt(str(seed_user.username))

    # Remove the header from the JWT
    jwt: str = jwt.split(".")[1]

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_002_anomalous_bad_token_missing_payload(
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 002 - Anomalous
    Conditions: JWT is missing its payload
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    jwt: str = generate_jwt(str(seed_user.username))

    # Remove the payload from the JWT
    jwt: str = jwt.split(".")[0] + "." + jwt.split(".")[2]

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_003_anomalous_bad_token_missing_signature(
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 003 - Anomalous
    Conditions: JWT is missing its signature
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    jwt: str = generate_jwt(str(seed_user.username))

    # Remove the signature from the JWT
    jwt: str = jwt.rsplit(".", 1)[0] + "."

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_004_anomalous_bad_token_extra_data(
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 004 - Anomalous
    Conditions: Token contains extra data beyond header, payload, and signature
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    jwt: str = generate_jwt(str(seed_user.username))

    # Add extra data to the JWT
    jwt += ".extra"

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_005_anomalous_bad_token_no_alg(
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 005 - Anomalous
    Conditions: No algorithm specified in header
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    jwt: str = generate_jwt(str(seed_user.username))

    # Remove the algorithm from the header

    jwt: str
    header: str
    payload: str
    header, payload, _ = jwt.split(".")
    header_data: Any = json.loads(base64.urlsafe_b64decode(header + "==").decode())
    header_data.pop("alg", None)  # Remove the 'alg' field
    new_header: str = (
        base64.urlsafe_b64encode(json.dumps(header_data).encode()).rstrip(b"=").decode()
    )

    # Construct the JWT without the 'alg' field in the header
    jwt = new_header + "." + payload + "."

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_006_anomalous_bad_token_wrong_alg(
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 006 - Anomalous
    Conditions: Wrong algorithm specified in header
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    jwt = generate_jwt(str(seed_user.username))

    # Change the algorithm in the header
    jwt: str
    header: str
    payload: str
    signature: str
    header, payload, signature = jwt.split(".")
    header_data: Any = json.loads(base64.urlsafe_b64decode(header + "==").decode())
    header_data["alg"] = "HS512"
    new_header: str = (
        base64.urlsafe_b64encode(json.dumps(header_data).encode()).rstrip(b"=").decode()
    )

    # Construct the JWT with the wrong algorithm in the header
    jwt: str = new_header + "." + payload + "." + signature

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_007_anomalous_bad_token_invalid_json(
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 007 - Anomalous
    Conditions: The contents of the payload is not valid JSON
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    jwt = generate_jwt(str(seed_user.username))

    # Change the payload to invalid JSON
    jwt: str
    header: str
    payload: str
    signature: str
    header, payload, signature = jwt.split(".")
    payload = "invalid"
    jwt = header + "." + payload + "." + signature

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_008_anomalous_invalid_token_expired(
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 008 - Anomalous
    Conditions: Token is expired
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    jwt: str = generate_jwt(str(seed_user.username), expiration=-1)

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_009_anomalous_invalid_token_missing_username(
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 009 - Anomalous
    Conditions: The token payload is missing a username
    Result: HTTP 401 - Invalid bearer token
    """
    # Calculate the expiration time
    expiration_time: datetime = datetime.now(timezone.utc) + timedelta(
        seconds=int(test_jwt_expiration_time)
    )

    # Create the payload with the subject, issued at, and expiration time
    payload: dict[str, str | datetime] = {
        "sub": "",
        "iat": datetime.now(timezone.utc),  # Issued at time
        "exp": expiration_time,  # Expiration time
    }

    # Generate the JWT
    token: str = jwt.encode(  # type: ignore
        payload, get_secret_key(), algorithm="HS256"
    )

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        await get_user_from_jwt(token, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_010_anomalous_invalid_token_invalid_username(
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 010 - Anomalous
    Conditions: The specified username does not exist
    Result: HTTP 401 - Invalid bearer token
    """
    # Calculate the expiration time
    expiration_time: datetime = datetime.now(timezone.utc) + timedelta(
        seconds=int(test_jwt_expiration_time)
    )

    # Create the payload with the subject, issued at, and expiration time
    payload: dict[str, str | datetime] = {
        "sub": "invalid-username",
        "iat": datetime.now(timezone.utc),  # Issued at time
        "exp": expiration_time,  # Expiration time
    }

    # Generate the JWT
    token: str = jwt.encode(  # type: ignore
        payload, get_secret_key(), algorithm="HS256"
    )

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        await get_user_from_jwt(token, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_011_anomalous_invalid_signature(
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 011 - Anomalous
    Conditions: The signature does not match the server's signature
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    jwt: str = generate_jwt(str(seed_user.username))

    # Change the signature
    jwt: str
    header: str
    payload: str
    signature: str
    header, payload, signature = jwt.split(".")
    signature = "invalid"
    jwt = header + "." + payload + "." + signature

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_012_anomalous_invalid_secret_key(
    monkeypatch: pytest.MonkeyPatch,
    seed_user: User,
    test_db: AsyncSession,
    test_jwt_secret_key: str,
    test_jwt_expiration_time: str,
) -> None:
    """
    Test 012 - Anomalous
    Conditions: The secret key does not match the server's secret key
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    jwt: str = generate_jwt(str(seed_user.username))

    # Change the secret key
    new_secret_key: str = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", new_secret_key)

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)
