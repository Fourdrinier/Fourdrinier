"""
build_dockerfile.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Build a Dockerfile as a string

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os
import textwrap


async def build_dockerfile(
    jdk_version: int, loader_url: str, server_port: int, min_memory: int, max_memory: int
) -> str:
    """
    Build a Dockerfile as a string
    """

    content: str = f"""
    FROM openjdk:{jdk_version}

    # Set the working directory of the image
    WORKDIR /server

    # Download the server jar
    ADD {loader_url} /server/server.jar

    # Expose the port for incoming connections
    EXPOSE {server_port}

    # Run the server
    CMD java -Xms{min_memory}M -Xmx{max_memory}M -jar server.jar
    """
    return textwrap.dedent(content).strip()
