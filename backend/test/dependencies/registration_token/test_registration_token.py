"""
test_registration_token.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test for the registration token dependency

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os
import pytest
from app.dependencies.registration_token import generate_registration_token


@pytest.mark.asyncio
async def test_generate_registration_token_000_nominal_first_time_startup(
    monkeypatch, test_storage
):
    """
    Test 000 - Nominal
    Conditions: First time start-up
    Result: Token generated and written to file
    """

    # Mock the secrets.token_hex function
    def mock_token_hex(*args, **kwargs):
        return "test_token"

    # Mock the secrets.token_hex function
    monkeypatch.setattr("secrets.token_hex", mock_token_hex)

    # Set the environment variable for the registration token file
    registration_token_file = os.path.join(test_storage, "registration_token")
    monkeypatch.setenv("REGISTRATION_TOKEN_FILE", registration_token_file)

    # Run the function
    token = generate_registration_token()

    # Check the results
    assert token == "test_token"
    with open(registration_token_file) as f:
        assert f.read() == "test_token"


@pytest.mark.asyncio
async def test_generate_registration_token_001_nominal_existing_token_file(
    monkeypatch, test_storage
):
    """
    Test 001 - Nominal
    Conditions: Token file exists
    Result: Token file overwritten
    """

    # Mock the secrets.token_hex function
    def mock_token_hex(*args, **kwargs):
        return "test_token"

    # Mock the secrets.token_hex function
    monkeypatch.setattr("secrets.token_hex", mock_token_hex)

    # Generate a token file
    registration_token_file = os.path.join(test_storage, "registration_token")
    with open(registration_token_file, "w") as f:
        f.write("old_token")

    # Ensure the file was created correctly
    assert os.path.exists(registration_token_file)
    assert open(registration_token_file).read() == "old_token"

    # Set the environment variable for the registration token file
    monkeypatch.setenv("REGISTRATION_TOKEN_FILE", registration_token_file)

    # Run the function
    token = generate_registration_token()

    # Check the results
    assert token == "test_token"
    with open(registration_token_file) as f:
        assert f.read() == "test_token"
