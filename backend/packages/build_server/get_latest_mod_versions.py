import asyncio

from fastapi import HTTPException

from backend.packages.modrinth.versions import (
    get_latest_compatible_version,
    NoCompatibleVersionException,
)


async def get_latest_mod_versions(project_ids, loader, game_version):
    latest_versions = []
    for project_id in project_ids:
        try:
            version = await get_latest_compatible_version(
                project_id, loader, game_version
            )
        except NoCompatibleVersionException as e:
            raise HTTPException(status_code=404, detail=str(e))
        latest_version = {"project_id": project_id, "version": version}
        latest_versions.append(latest_version)
        await asyncio.sleep(0.2)
    return latest_versions
