"""
generate_jwt.py

@Author: Ethan Brown - ethan@ewbronwtech.com

This file contains the function to generate a JWT token for a user

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import jwt
from datetime import datetime, timedelta
from backend.app.dependencies.core.jwt.get_secret_key import get_secret_key
from backend.app.dependencies.core.jwt.get_jwt_expiration import get_jwt_expiration_time


def generate_jwt(username: str, expiration: int | None = None) -> str:
    # Set the expiration time to the provided value or get it from the default function
    if expiration is None:
        expiration = get_jwt_expiration_time()

    # Calculate the expiration time
    expiration_time = datetime.utcnow() + timedelta(seconds=expiration)

    # Create the payload with the subject, issued at, and expiration time
    payload: dict[str, str | datetime] = {
        "sub": username,
        "iat": datetime.utcnow(),  # Issued at time
        "exp": expiration_time,  # Expiration time
    }

    # Generate the JWT
    token: str = jwt.encode(  # type: ignore
        payload, get_secret_key(), algorithm="HS256"
    )

    return token
