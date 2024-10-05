"""
build_dockerfile.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Build a Dockerfile as a string

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os
import docker
import io
import tarfile
import textwrap
import docker.errors
from docker.models.images import Image


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


async def build_image(dockerfile_content: str, image_name: str) -> str:
    """
    Build a Docker image from a Dockerfile
    """
    client = docker.DockerClient(base_url=os.getenv("DOCKER_HOST"))

    # Create an in-memory bytes buffer to store the tar archive
    tar_stream = io.BytesIO()

    # Create an in-memory tar archive containing the Dockerfile
    with tarfile.TarFile(fileobj=tar_stream, mode="w") as tar:
        dockerfile_data = dockerfile_content.encode("utf-8")
        dockerfile_info = tarfile.TarInfo(name="Dockerfile")
        dockerfile_info.size = len(dockerfile_data)

        # Add the Dockerfile content to the tar archive
        tar.addfile(tarinfo=dockerfile_info, fileobj=io.BytesIO(dockerfile_data))

    # Reset the stream position to the beginning
    tar_stream.seek(0)

    # Build the Docker image using the in-memory tar archive
    image: Image
    image, logs = client.images.build(fileobj=tar_stream, custom_context=True, tag=image_name)

    # Print build logs
    for log in logs:
        if "stream" in log:
            print(log["stream"].strip())

    assert image.id
    print(f"Image '{image_name}' built successfully.")
    return image.id
