from backend.packages.fabric.get_latest_fabric_version import (
    get_latest_loader_version,
    get_latest_launcher_version,
)


async def get_fabric_url(game_version):
    loader_version = await get_latest_loader_version(game_version)
    launcher_version = await get_latest_launcher_version()
    api_url = "https://meta.fabricmc.net/v2/versions/loader"
    loader_url = (
        f"{api_url}/{game_version}/{loader_version}/{launcher_version}/server/jar"
    )
    return loader_url
