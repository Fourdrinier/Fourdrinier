"""
build_server.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Builds a server

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import logging
from backend.app.db.models import Server

from backend.app.dependencies.build_server.docker.build_docker import build_docker


# Configure logging
logger: logging.Logger = logging.getLogger(__name__)


def build_server(server: Server) -> None:
    """
    Build a server
    """
    logger.debug(
        f"Building server {server.name} with loader {server.loader} "
        "using strategy Docker"
    )

    return None
