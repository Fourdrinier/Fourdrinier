import httpx
from fastapi import HTTPException


async def get_latest_mod_version(mod_id, game_version):
    # Get the list of available versions of a mod
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'https://api.modrinth.com/v2/project/{mod_id}/version?game_versions=["{game_version}"]'
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Unable to locate specified mod",
            )
        latest_version = response.json()[0]
        url = latest_version["files"][0]["url"]
    return {"id": latest_version["id"], "url": url}
