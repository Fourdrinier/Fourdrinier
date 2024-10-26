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


async def start_container(image_name: str) -> str:
    """
    Start a server container
    """
    client = docker.DockerClient(base_url=os.getenv("DOCKER_HOST"))
    image: Image = client.images.get(image_name)
    container: Container = client.containers.run(image, detach=True)
    if container.id is None:
        raise RuntimeError("Failed to start container")

    return container.id
