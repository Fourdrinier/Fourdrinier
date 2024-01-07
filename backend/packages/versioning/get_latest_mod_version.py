import httpx
from fastapi import HTTPException


async def get_latest_mod_version(mod_id, loader, game_version):
    # Get the list of available versions of a mod
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'https://api.modrinth.com/v2/project/{mod_id}/version?game_versions=["{game_version}"]'
        )
        if response.status_code != 200:
            print(response)
            raise HTTPException(
                status_code=404,
                detail=f"Unable to locate specified mod {mod_id}",
            )
        latest_version = None
        for version in response.json():
            if loader in version["loaders"]:
                latest_version = version
                break
        if latest_version is None:
            raise NoCompatibleVersionException
        url = latest_version["files"][0]["url"]
    return {"id": latest_version["id"], "url": url}


class NoCompatibleVersionException(Exception):
    pass
