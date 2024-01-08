from backend.packages.fabric.get_fabric_url import get_fabric_url


async def get_jarfile_url(loader, game_version):
    url = None
    match loader:
        case "fabric":
            url = await get_fabric_url(game_version)

    return url
