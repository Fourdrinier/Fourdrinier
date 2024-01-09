import httpx
from fastapi import HTTPException


async def get_versions(project_id, game_versions):
    # This string casting must be done this way such that the elements
    # will appear with double quotes around them in the API request
    game_versions_string = (
        "[" + ", ".join(f'"{game_version}"' for game_version in game_versions) + "]"
    )
    async with httpx.AsyncClient() as client:
        try:
            request = f"https://api.modrinth.com/v2/project/{project_id}/version?game_versions={game_versions_string}"
            response = await client.get(request)
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=500, detail=f"The following request timed out: {request}"
            )
        if response.status_code != 200:
            raise NoVersionFoundException(project_id, game_versions)
    versions = response.json()
    return versions


async def get_latest_compatible_version(project_id, loader, game_version):
    versions = await get_versions(project_id, [game_version])
    latest_version = None
    for version in versions:
        if loader in version["loaders"]:
            latest_version = version
            break
    if latest_version is None:
        raise NoCompatibleVersionException(project_id, loader, game_version)
    return latest_version


class NoVersionFoundException(Exception):
    def __init__(self, project_id, game_versions):
        message = f"No versions found for project ID {project_id} within game versions {game_versions}"
        super().__init__(message)


class NoCompatibleVersionException(Exception):
    def __init__(self, project_id, loader, game_version):
        message = f"No versions found for project ID {project_id} for {loader} Minecraft version {game_version}"
        super().__init__(message)
