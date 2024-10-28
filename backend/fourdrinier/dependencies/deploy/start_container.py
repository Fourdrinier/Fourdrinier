"""
start_container.py

Start a server container

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os

import docker
import docker.errors
from docker.models.containers import Container
from docker.models.images import Image


async def start_container() -> str:
    """
    Start a server container
    """
    client = docker.DockerClient(base_url=os.getenv("DOCKER_HOST"))

    try:
        image: Image = client.images.get("itzg/minecraft-server:java17-alpine")
    except docker.errors.ImageNotFound:
        image: Image = client.images.pull("itzg/minecraft-server:java17-alpine")

    container: Container = client.containers.run(
        image,
        detach=True,
        environment={"EULA": "true", "VERSION": "1.20.1"},
        tty=True,  # Allocates a pseudo-TTY
        stdin_open=True,  # Keeps stdin open, equivalent to -i
        ports={"25565/tcp": 25565},  # Port forward host:container
    )
    if container.id is None:
        raise RuntimeError("Failed to start container")

    return container.id
