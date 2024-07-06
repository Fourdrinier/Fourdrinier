"""
auth.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Contains dependencies for authentication

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import bcrypt


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


async def get_password_hash(password: str) -> str:
    """
    Get a hashed password
    """
    hashed_password: str = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    return hashed_password
