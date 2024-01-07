import httpx
from fastapi import HTTPException

from backend.packages.versioning.get_latest_mod_version import (
    get_latest_mod_version,
    NoCompatibleVersionException,
)


async def get_mod_dependencies(
    version_id, game_version, required_dependencies=None, optional_dependencies=None
):
    if required_dependencies is None:
        required_dependencies = []
    if optional_dependencies is None:
        optional_dependencies = []

    # Initialize lists of new dependencies. Only these mods will have their own dependencies scanned
    new_required_dependencies = []
    new_optional_dependencies = []

    # Get the dependencies of the specified version of a mod
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.modrinth.com/v2/version/{version_id}")
        if response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Unable to locate specified version",
            )
        dependencies_objects = response.json()["dependencies"]

    # Get the latest version of each of these dependencies and sort them by optional and required
    for dependency_object in dependencies_objects:
        if dependency_object["project_id"] == "9CJED7xi":
            continue
        try:
            latest_mod_version = await get_latest_mod_version(
                dependency_object["project_id"], game_version
            )
        except NoCompatibleVersionException:
            raise HTTPException(
                status_code=404,
                detail=f'There is no available version of dependency ID: {dependency_object["project_id"]} compatible with Fabric Minecraft version {game_version}',
            )
        match dependency_object["dependency_type"]:
            case "required":
                if latest_mod_version not in required_dependencies:
                    new_required_dependencies.append(latest_mod_version)
            case "optional":
                if latest_mod_version not in optional_dependencies:
                    new_optional_dependencies.append(latest_mod_version)

    # Add the new dependencies to the existing dependencies to prevent them from being scanned in recursive calls
    required_dependencies.extend(new_required_dependencies)
    optional_dependencies.extend(new_optional_dependencies)

    # Recurse through the dependencies to collect their dependencies
    for mod_version in new_required_dependencies:
        required_dependencies, optional_dependencies = await get_mod_dependencies(
            mod_version["id"],
            game_version,
            required_dependencies,
            optional_dependencies,
        )
    for mod_version in new_optional_dependencies:
        required_dependencies, optional_dependencies = await get_mod_dependencies(
            mod_version["id"],
            game_version,
            required_dependencies,
            optional_dependencies,
        )

    return required_dependencies, optional_dependencies
