"""
get_jwt_expiration.py

@Author: Ethan Brown - ethan@ewbrowntech.com

This file contains the function to get the expiration time for a JWT token

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os


def get_jwt_expiration_time() -> int:
    """Get the expiration time for a JWT token"""
    # Get the expiration time from the environment
    expiration_time = os.getenv("JWT_EXPIRATION_TIME")

    # Ensure that the expiration time is not empty
    if expiration_time is None or expiration_time == "":
        raise EnvironmentError(
            "The environment variable JWT_EXPIRATION_TIME cannot be empty"
        )

    # Ensure that the expiration time is an integer
    if not expiration_time.isdigit():
        raise ValueError(
            "The environment variable JWT_EXPIRATION_TIME must be an integer"
        )

    # Ensure that the expiration time is at least 1 minute
    if int(expiration_time) < 1:
        raise ValueError(
            "The environment variable JWT_EXPIRATION_TIME must be at least 1 minute"
        )

    return expiration_time
