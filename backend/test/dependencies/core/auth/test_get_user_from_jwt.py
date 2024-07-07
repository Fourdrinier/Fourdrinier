"""
test_get_user_from_jwt.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the functionality of get_user_from_jwt()

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import pytest

import jwt
import os
import secrets
from datetime import datetime, timedelta
import base64
import json

from backend.app.app import app
from backend.app.dependencies.core.auth.generate_jwt import generate_jwt
from backend.app.dependencies.jwt.get_user_from_jwt import get_user_from_jwt
from backend.app.dependencies.jwt.get_secret_key import get_secret_key
from backend.app.dependencies.jwt.get_jwt_expiration import get_jwt_expiration_time

from backend.app.db.session import get_db


@pytest.mark.asyncio
async def test_get_user_from_jwt_000_nominal(
    seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 000 - Nominal
    Conditions: JWT is valid
    Result: User object returned
    """
    # Generate a valid JWT
    username = seed_user.username
    jwt = generate_jwt(username)

    # Ensure that the user object is returned
    user = await get_user_from_jwt(jwt, test_db)
    assert user
    assert user.username == username


@pytest.mark.asyncio
async def test_get_user_from_jwt_001_bad_token_missing_header(
    seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 001 - Bad token - missing header
    Conditions: JWT is missing header
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    username = seed_user.username
    jwt = generate_jwt(username)

    # Remove the header from the JWT
    jwt = jwt.split(".")[1]

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        user = await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_002_anomalous_bad_token_missing_payload(
    seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 002 - Anomalous
    Conditions: JWT is missing its payload
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    username = seed_user.username
    jwt = generate_jwt(username)

    # Remove the payload from the JWT
    jwt = jwt.split(".")[0] + "." + jwt.split(".")[2]

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        user = await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_003_anomalous_bad_token_missing_signature(
    seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 003 - Anomalous
    Conditions: JWT is missing its signature
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    username = seed_user.username
    jwt = generate_jwt(username)

    # Remove the signature from the JWT
    jwt = jwt.rsplit(".", 1)[0] + "."

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        user = await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_004_anomalous_bad_token_extra_data(
    seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 004 - Anomalous
    Conditions: Token contains extra data beyond header, payload, and signature
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    username = seed_user.username
    jwt = generate_jwt(username)

    # Add extra data to the JWT
    jwt += ".extra"

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        user = await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_005_anomalous_bad_token_no_alg(
    seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 005 - Anomalous
    Conditions: No algorithm specified in header
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    username = seed_user.username
    jwt = generate_jwt(username)

    # Remove the algorithm from the header
    header, payload, signature = jwt.split(".")
    header_data = json.loads(base64.urlsafe_b64decode(header + "==").decode())
    header_data.pop("alg", None)  # Remove the 'alg' field
    new_header = (
        base64.urlsafe_b64encode(json.dumps(header_data).encode()).rstrip(b"=").decode()
    )

    # Construct the JWT without the 'alg' field in the header
    jwt = new_header + "." + payload + "."

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        user = await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_006_anomalous_bad_token_wrong_alg(
    seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 006 - Anomalous
    Conditions: Wrong algorithm specified in header
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    username = seed_user.username
    jwt = generate_jwt(username)

    # Change the algorithm in the header
    header, payload, signature = jwt.split(".")
    header_data = json.loads(base64.urlsafe_b64decode(header + "==").decode())
    header_data["alg"] = "HS512"
    new_header = (
        base64.urlsafe_b64encode(json.dumps(header_data).encode()).rstrip(b"=").decode()
    )

    # Construct the JWT with the wrong algorithm in the header
    jwt = new_header + "." + payload + "." + signature

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        user = await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_007_anomalous_bad_token_invalid_json(
    seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 007 - Anomalous
    Conditions: The contents of the payload is not valid JSON
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    username = seed_user.username
    jwt = generate_jwt(username)

    # Change the payload to invalid JSON
    header, payload, signature = jwt.split(".")
    payload = "invalid"
    jwt = header + "." + payload + "." + signature

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        user = await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_008_anomalous_invalid_token_expired(
    seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 008 - Anomalous
    Conditions: Token is expired
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    username = seed_user.username
    jwt = generate_jwt(username, expiration=-1)

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        user = await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_009_anomalous_invalid_token_missing_username(
    seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 009 - Anomalous
    Conditions: The token payload is missing a username
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    username = seed_user.username

    # Calculate the expiration time
    expiration_time = datetime.utcnow() + timedelta(
        seconds=int(test_jwt_expiration_time)
    )

    # Create the payload with the subject, issued at, and expiration time
    payload = {
        "sub": "",
        "iat": datetime.utcnow(),  # Issued at time
        "exp": expiration_time,  # Expiration time
    }

    # Generate the JWT
    token = jwt.encode(payload, get_secret_key(), algorithm="HS256")

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        user = await get_user_from_jwt(token, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_010_anomalous_invalid_token_invalid_username(
    seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 010 - Anomalous
    Conditions: The specified username does not exist
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    username = seed_user.username

    # Calculate the expiration time
    expiration_time = datetime.utcnow() + timedelta(
        seconds=int(test_jwt_expiration_time)
    )

    # Create the payload with the subject, issued at, and expiration time
    payload = {
        "sub": "invalid-username",
        "iat": datetime.utcnow(),  # Issued at time
        "exp": expiration_time,  # Expiration time
    }

    # Generate the JWT
    token = jwt.encode(payload, get_secret_key(), algorithm="HS256")

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        user = await get_user_from_jwt(token, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_011_anomalous_invalid_signature(
    seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 011 - Anomalous
    Conditions: The signature does not match the server's signature
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    username = seed_user.username
    jwt = generate_jwt(username)

    # Change the signature
    header, payload, signature = jwt.split(".")
    signature = "invalid"
    jwt = header + "." + payload + "." + signature

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        user = await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)


@pytest.mark.asyncio
async def test_get_user_from_jwt_012_anomalous_invalid_secret_key(
    monkeypatch, seed_user, test_db, test_jwt_secret_key, test_jwt_expiration_time
):
    """
    Test 012 - Anomalous
    Conditions: The secret key does not match the server's secret key
    Result: HTTP 401 - Invalid bearer token
    """
    # Generate a valid JWT
    username = seed_user.username
    jwt = generate_jwt(username)

    # Change the secret key
    new_secret_key = secrets.token_hex(32)
    monkeypatch.setenv("JWT_SECRET_KEY", new_secret_key)

    # Ensure that the correct exception is raised
    with pytest.raises(Exception) as e:
        user = await get_user_from_jwt(jwt, test_db)
    assert "Invalid bearer token" in str(e.value)
