"""
get_password_hash.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Contains dependencies for getting password hashes

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import bcrypt


async def get_password_hash(password: str) -> str:
    """
    Get a hashed password
    """
    hashed_password: str = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    return hashed_password
