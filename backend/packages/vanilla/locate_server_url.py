import httpx

from fastapi import HTTPException


async def locate_server_url(game_version):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Unable to access Minecraft version manifest",
            )

    data = response.json()
    version_metadata_url = None
    for version in data["versions"]:
        if version["id"] == game_version:
            version_metadata_url = version["url"]
            break
    if version_metadata_url is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to locate specified version of Minecraft within manifest",
        )

    # Use the metadata for the specified Minecraft version to locate the url for its server .jar
    async with httpx.AsyncClient() as client:
        response = await client.get(version_metadata_url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Unable to access metadata for given version of Mineacraft",
            )
    data = response.json()
    server_download_url = data["downloads"]["server"]["url"]

    return server_download_url
