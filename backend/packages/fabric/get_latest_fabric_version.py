import httpx


async def get_latest_loader_version(game_version):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://meta.fabricmc.net/v2/versions/loader/{game_version}"
        )
        if response.status_code != 200:
            raise NoCompatibleFabricLoaderException(game_version)
    return response.json()[0]["loader"]["version"]


async def get_latest_launcher_version():
    # 1) Get all available versions of the Fabric server launcher
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://meta.fabricmc.net/v2/versions/installer")
        if response.status_code != 200:
            raise NoCompatibleFabricLauncherException
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


class NoCompatibleFabricLoaderException(Exception):
    def __init__(self, game_version):
        message = f"No compatible version of the Fabric loader was found for Minecraft version {game_version}"
        super().__init__(message)


class NoCompatibleFabricLauncherException(Exception):
    def __init__(self):
        message = f"No compatible version of the Fabric launcher was found."
        super().__init__(message)
