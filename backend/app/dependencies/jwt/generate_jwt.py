"""
generate_jwt.py

@Author: Ethan Brown - ethan@ewbronwtech.com

This file contains the function to generate a JWT token for a user

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import jwt
from app.dependencies.jwt.get_secret_key import get_secret_key


def generate_jwt(username: str) -> str:
    """Generate a JWT token for a user"""
    # Ensure that a username is provided and is a string
    if username is None or username == "" or not isinstance(username, str):
        raise ValueError(
            f"'username' must be of type <class 'str'>, not {type(username)}"
        )

    # Generate the JWT
    payload = {"sub": username}
    token = jwt.encode(payload, get_secret_key(), algorithm="HS256")

    return token
