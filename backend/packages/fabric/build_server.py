"""
fabric/build_server.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 5 JAN 23

Build a server image given its settings
"""

import docker
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import Playset
from backend.packages.build_server.build_dockerfile import build_dockerfile
from backend.packages.storage.get_server_directory import get_server_directory


async def build_server(server, db: AsyncSession):
    server = {
        "id": server.id,
        "name": server.name,
        "game_version": server.game_version,
        "loader": server.loader,
        "playset": await db.get(
            Playset,
            server.playset.id,
            populate_existing=True,
            options=[selectinload(Playset.mods)],
        ),
        "port": server.port,
        "eula": server.eula,
        "allocated_memory": server.allocated_memory,
    }
    await build_dockerfile(server)
    print("Dockerfile build successful")
    image_name = await build_docker_image(server)

    return {"image_name": image_name}


async def build_docker_image(server):
    server_directory = await get_server_directory(server["id"])
    image_name = "fabric-" + server["id"]
    # Create a Docker client
    with docker.APIClient(base_url="unix://var/run/docker.sock") as low_level_client:
        # Stream the build output
        response = low_level_client.build(
            path=server_directory, tag=image_name, decode=True
        )

    # Compile the build log
    build_log = []
    for item in response:
        message = item.get("stream") or item.get("aux")
        if message and message != "\n":
            build_log.append(message)

    # If the build failed, remove the image. Otherwise, return the image name
    if len(build_log) > 0 and "Successfully built" in build_log[-2]:
        return image_name
    else:
        with docker.from_env() as client:
            client.images.remove(image=image_name)
        raise HTTPException(status_code=500, detail="Failed to build Docker image")
