"""
get_secret_key.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Get the secret key for the JWT token

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os


def get_secret_key() -> str:
    """Get the secret key for the JWT token"""
    # Get the secret key from the environment
    secret_key = os.getenv("JWT_SECRET_KEY")

    # Ensure that the secret key is not empty
    if secret_key is None or secret_key == "":
        raise EnvironmentError(
            "The environment variable JWT_SECRET_KEY cannot be empty"
        )

    # Ensure that the secret key is at least 256 bits (64 hexadecimal characters) long
    if len(secret_key) < 64:
        raise ValueError(
            "The environment variable JWT_SECRET_KEY must be at least 256 bits (64 hexadecimal characters) long"
        )

    return secret_key
