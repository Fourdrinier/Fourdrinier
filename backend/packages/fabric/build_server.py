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
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import Playset
from backend.packages.fabric.get_latest_mod_version import get_latest_mod_version
from backend.packages.fabric.get_mod_depencies import get_mod_dependencies
from backend.packages.storage.get_server_directory import get_server_directory


async def build_server(server, db: AsyncSession):
    server = {
        "id": server.id,
        "name": server.name,
        "game_version": server.game_version,
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
    image_name = await build_docker_image(server)

    return {"image_name": image_name}


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


async def build_dockerfile(server):
    java_requirement = await get_java_requirement(server["game_version"])
    loader_version = await get_loader_version(server["game_version"])
    launcher_version = await get_launcher_version()
    api_url = "https://meta.fabricmc.net/v2/versions/loader"
    loader_url = f'{api_url}/{server["game_version"]}/{loader_version}/{launcher_version}/server/jar'

    # Get the URL for the latest version of the Fabric API mod, as it is almost always required
    latest_fabric_api_mod_version = await get_latest_mod_version(
        "P7dR8mSH", server["game_version"]
    )
    fabric_api_mod_url = latest_fabric_api_mod_version["url"]

    # Open the boilerplate Dockerfile
    with open(
        os.path.join(os.path.dirname(__file__), "boilerplate", "Dockerfile"), "r"
    ) as boilerplate_dockerfile:
        content = boilerplate_dockerfile.read()

    # Compile version ID's and dependencies for each mod
    mod_version_ids = []
    mod_urls = []
    required_dependencies = []
    optional_dependencies = []
    for mod in server["playset"].mods:
        # Get the latest version of the mod
        version = await get_latest_mod_version(mod.id, server["game_version"])
        mod_version_ids.append(version["id"])
        mod_urls.append(version["url"])

        # Recursively compile the mod's dependencies
        (
            version_required_dependencies,
            version_optional_dependencies,
        ) = await get_mod_dependencies(version["id"], server["game_version"])

        # Add mod required dependencies to the global required dependencies
        for dependency in version_required_dependencies:
            if dependency not in required_dependencies:
                required_dependencies.append(dependency)

        # Add mod required dependencies to the global optional dependencies
        for dependency in version_optional_dependencies:
            if dependency not in optional_dependencies:
                optional_dependencies.append(dependency)

    # Compile URLs for required dependencies
    required_dependency_urls = []
    for dependency in required_dependencies:
        required_dependency_urls.append(dependency["url"])

    # Compile URLs for optional dependencies
    optional_dependency_urls = []
    for dependency in optional_dependencies:
        optional_dependency_urls.append(dependency["url"])

    # Create command block for downloading specified mods
    download_mod_block = ""
    for mod_url in mod_urls:
        download_mod_block += f'ADD "{mod_url}" /downloads\n'

    # Create command block for downloading required dependencies
    download_req_dep_block = ""
    for required_dependency_url in required_dependency_urls:
        download_req_dep_block += f'ADD "{required_dependency_url}" /downlaods\n'

    # Create command block for downloading required dependencies
    download_opt_dep_block = ""
    for optional_dependency_url in optional_dependency_urls:
        download_opt_dep_block += f'ADD "{optional_dependency_url}" /downloads\n'

    # Tailor the boilerplate Dockerfile to the server
    tailored_dockerfile = (
        content.replace("${JAVA_VERSION}", str(java_requirement))
        .replace("${GAME_VERSION}", server["game_version"])
        .replace("${LOADER_URL}", loader_url)
        .replace("${FABRIC_API_URL}", fabric_api_mod_url)
        .replace("${MOD_DOWNLOADS}", download_mod_block)
        .replace("${REQUIRED_DEPENDENCY_DOWNLOADS}", download_req_dep_block)
        .replace("${OPTIONAL_DEPENDENCY_DOWNLOADS}", download_opt_dep_block)
        .replace("${EULA}", str(server["eula"]).lower())
    )

    # Get the path to the server's storage directory
    server_directory = await get_server_directory(server["id"])
    Path(server_directory).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(server_directory, "Dockerfile"), "w") as dockerfile:
        dockerfile.write(tailored_dockerfile)


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
    if "Successfully built" in build_log[-2]:
        return image_name
    else:
        with docker.from_env() as client:
            client.images.remove(image=image_name)
        raise HTTPException(status_code=500, detail="Failed to build Docker image")
