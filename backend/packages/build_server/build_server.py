from sqlalchemy.orm import selectinload

from backend.models import Playset
from backend.packages.build_server.build_docker_image import build_docker_image
from backend.packages.build_server.build_dockerfile import build_dockerfile


async def build_server(server, db):
    server = {
        "id": server.id,
        "name": server.name,
        "game_version": server.game_version,
        "loader": server.loader,
        "playset": await db.get(
            Playset,
            server.playset.id,
            populate_existing=True,
            options=[selectinload(Playset.mods)],
        ),
        "port": server.port,
        "eula": server.eula,
        "allocated_memory": server.allocated_memory,
    }

    await build_dockerfile(server)
    print("Dockerfile build successful")
    image_name = await build_docker_image(server)

    return {"image_name": image_name}
