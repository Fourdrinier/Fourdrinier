import os
from pathlib import Path

import docker

from backend.packages.storage.get_server_directory import get_server_directory


async def run_new_container(server):
    # Ensure a world and mod directory is present
    server_directory = await get_server_directory(server.id)
    world_folder_path = os.path.join(server_directory, "world")
    Path(world_folder_path).mkdir(parents=True, exist_ok=True)
    mod_folder_path = os.path.join(server_directory, "mods")
    Path(mod_folder_path).mkdir(parents=True, exist_ok=True)

    # Now get the host path for the server directory
    server_directory = await get_server_directory(server.id, host=True)
    world_folder_path = os.path.join(server_directory, "world")
    mod_folder_path = os.path.join(server_directory, "mods")

    # Define image name, necessary port and volume mappings
    image_name = server.loader + "-" + server.id
    port_mapping = {"25565/tcp": server.port}
    volume_mapping = {
        world_folder_path: {
            "bind": "/minecraft/world",
            "propagation": "rshared",
        },
        mod_folder_path: {
            "bind": "/minecraft/mods",
            "propagation": "rshared",
        },
    }

    # Run the Docker container
    client = docker.from_env()
    container = client.containers.run(
        image_name,
        detach=True,
        name=image_name,
        environment={"ALLOCATED_RAM": str(server.allocated_memory) + "M"},
        ports=port_mapping,
        volumes=volume_mapping,
        stdin_open=True,
    )
    return {"container_id": container.id}
