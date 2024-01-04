"""
fabric/build_server.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 3 JAN 23

Build a server image given its settings
"""
import json
import os
from pathlib import Path

import docker
import httpx
from fastapi import HTTPException

from backend.packages.storage.get_server_directory import get_server_directory


async def build_server(server):
    server = {
        "id": server.id,
        "name": server.name,
        "game_version": server.game_version,
        "playset": None,
        "port": server.port,
        "eula": server.eula,
        "allocated_memory": server.allocated_memory,
    }

    java_requirement = await get_java_requirement(server["game_version"])
    loader_version = await get_loader_version(server["game_version"])
    launcher_version = await get_launcher_version()
    loader_url = f'https://meta.fabricmc.net/v2/versions/loader/{server["game_version"]}/{loader_version}/{launcher_version}/server/jar'

    # Set up the basics of the Dockerfile
    dockerfile_content = [
        f"FROM openjdk:{java_requirement}",
        "WORKDIR /minecraft",
        f'ADD "{loader_url}" /minecraft/fabric.jar',
        f'RUN echo "eula={server["eula"]}" > /minecraft/eula.txt',
        f'EXPOSE {server["port"]}',
        f'CMD java -Xmx{server["allocated_memory"]}M -jar /minecraft/fabric.jar nogui',
    ]

    # Open the boilerplate Dockerfile
    with open(
        os.path.join(os.path.dirname(__file__), "boilerplate", "Dockerfile"), "r"
    ) as boilerplate_dockerfile:
        content = boilerplate_dockerfile.read()

    # Tailor the boilerplate Dockerfile to the server
    tailored_dockerfile = (
        content.replace("${JAVA_VERSION}", str(java_requirement))
        .replace("${GAME_VERSION}", server["game_version"])
        .replace("${LOADER_URL}", loader_url)
        .replace("${EULA}", str(server["eula"]).lower())
        .replace("${PORT}", str(server["port"]))
    )

    # Get the path to the server's storage directory
    server_directory = await get_server_directory(server["id"])
    Path(server_directory).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(server_directory, "Dockerfile"), "w") as dockerfile:
        dockerfile.write(tailored_dockerfile)

    # Create a Docker client
    client = docker.from_env()
    image_name = "fabric-" + server["id"]
    # The low-level API client gives more control and returns a generator
    low_level_client = docker.APIClient(base_url="unix://var/run/docker.sock")
    # Stream the build output
    response = low_level_client.build(
        path=server_directory, tag=image_name, decode=True
    )
    build_log = []
    for item in response:
        message = item.get("stream") or item.get("aux")
        if message and message != "\n":
            build_log.append(message)
    if "Successfully built" in build_log[-2]:
        return {"image_name": image_name}
    else:
        client.images.remove(image=image_name)
        raise HTTPException(status_code=500, detail="Failed to build Docker image")


async def get_java_requirement(game_version):
    with open(
        os.path.join(os.path.dirname(__file__), "java_compatibility.json"), "r"
    ) as file:
        java_compatability = json.load(file)
    return java_compatability[game_version]


async def get_loader_version(game_version):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://meta.fabricmc.net/v2/versions/loader/{game_version}"
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="No Fabric build found for supplied game version",
            )
    return response.json()[0]["loader"]["version"]


async def get_launcher_version():
    # 1) Get all available versions of the Fabric server launcher
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://meta.fabricmc.net/v2/versions/installer")
        if response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="No Fabric build found for supplied game version",
            )
    data = response.json()

    # 2) Find the newest stable release available
    newest_stable_version = None
    for launcher_version in data:
        if launcher_version.get("stable", False):
            newest_stable_version = launcher_version["version"]
            break

    # If there are no stable releases, simply use the newest release
    if newest_stable_version is None:
        newest_stable_version = data[0]["version"]

    return newest_stable_version
