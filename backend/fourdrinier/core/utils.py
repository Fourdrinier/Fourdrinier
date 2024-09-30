"""
config.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Utility functions for Fourdrinier.

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import secrets


async def generate_id() -> str:
    """
    Generate a unique 8-character ID.
    """
    return secrets.token_hex(4)
