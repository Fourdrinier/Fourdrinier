"""
get_server_directory.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Get the server directory

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os


async def get_server_directory(server_id: str, host: bool = False) -> str:
    """
    Get the server directory
    """
    storage_path: str = os.getenv("STORAGE_PATH", "/storage")
    return os.path.join(storage_path, server_id)
