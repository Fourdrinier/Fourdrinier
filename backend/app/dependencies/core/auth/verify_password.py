"""
verify_password.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Contains dependencies for verifying passwords

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
