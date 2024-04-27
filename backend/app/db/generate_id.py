"""
generate_id.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Generate a unique ID for a new object

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import secrets


def generate_id() -> str:
    """Generate a unique ID for a new object"""
    return secrets.token_hex(4)
