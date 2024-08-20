"""
build_docker.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Builds a server using Docker

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os
from backend.app.db.models import Server
from backend.app.dependencies.storage.get_server_directory import get_server_directory


async def build_docker(server: Server) -> None:
    """
    Build a server using Docker
    """
    # Get the Docker socket
    docker_socket: str = os.getenv("DOCKER_SOCKET", "/var/run/docker.sock")

    server_directory: str = await get_server_directory(server.id)

    return None
