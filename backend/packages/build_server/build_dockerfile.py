import json
import os
import shutil
from pathlib import Path

from backend.packages.build_server.get_jarfile_url import get_jarfile_url
from backend.packages.java.get_java_requirement import get_java_requirement
from backend.packages.server_properties.generate_properties import generate_properties
from backend.packages.storage.get_server_directory import get_server_directory


async def build_dockerfile(server):
    java_requirement = await get_java_requirement(server.loader, server.game_version)
    jarfile_url = await get_jarfile_url(server.loader, server.game_version)

    # Compile urls for projects
    mod_urls = []
    required_dependency_urls = []
    optional_dependency_urls = []
    for mod in server.server_mods:
        match mod.role:
            case "requested":
                mod_urls.append(mod.url)
            case "required_dependency":
                required_dependency_urls.append(mod.url)
            case "optional_dependency":
                optional_dependency_urls.append(mod.url)

    # Create command block for downloading specified mods
    download_mod_block = ""
    for mod_url in mod_urls:
        download_mod_block += f'ADD "{mod_url}" /downloads/\n'

    # Create command block for downloading required dependencies
    download_req_dep_block = ""
    for required_dependency_url in required_dependency_urls:
        download_req_dep_block += f'ADD "{required_dependency_url}" /downloads/\n'

    # Create command block for downloading required dependencies
    download_opt_dep_block = ""
    for optional_dependency_url in optional_dependency_urls:
        download_opt_dep_block += f'ADD "{optional_dependency_url}" /downloads/\n'

    # Open the boilerplate Dockerfile
    boilerplate_directory = os.path.join(os.path.dirname(__file__), "boilerplate")
    with open(
        os.path.join(boilerplate_directory, "Dockerfile"), "r"
    ) as boilerplate_dockerfile:
        content = boilerplate_dockerfile.read()

    # Tailor the boilerplate Dockerfile to the server
    tailored_dockerfile = (
        content.replace("${JAVA_VERSION}", str(java_requirement))
        .replace("${GAME_VERSION}", server.game_version)
        .replace("${LOADER}", server.loader.title())
        .replace("${LOADER_URL}", jarfile_url)
        .replace("${MOD_DOWNLOADS}", download_mod_block)
        .replace("${REQUIRED_DEPENDENCY_DOWNLOADS}", download_req_dep_block)
        .replace("${OPTIONAL_DEPENDENCY_DOWNLOADS}", download_opt_dep_block)
        .replace("${EULA}", str(server.eula).lower())
        .replace(
            "${SERVER_PROPERTIES}",
            '"' + await generate_properties(server) + '"',
        )
        .replace("${OPS}", '"' + str(json.loads(server.ops)["ops"]) + '"')
        .replace("${ALLOCATED_RAM}", str(server.allocated_memory) + "M")
    )

    # Get the path to the server's storage directory
    server_directory = await get_server_directory(server.id)
    Path(server_directory).mkdir(parents=True, exist_ok=True)

    # Write the Dockerfile
    with open(os.path.join(server_directory, "Dockerfile"), "w") as dockerfile:
        dockerfile.write(tailored_dockerfile)

    # Copy over the entrypoint.txt script
    shutil.copy(
        os.path.join(boilerplate_directory, "entrypoint.txt"),
        os.path.join(server_directory, "entrypoint.txt"),
    )

    # Ensure a world and mod directory is present
    world_folder_path = os.path.join(server_directory, "world")
    Path(world_folder_path).mkdir(parents=True, exist_ok=True)
    mod_folder_path = os.path.join(server_directory, "mods")
    Path(mod_folder_path).mkdir(parents=True, exist_ok=True)
