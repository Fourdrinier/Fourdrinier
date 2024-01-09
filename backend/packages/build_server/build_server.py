from backend.packages.build_server.build_docker_image import build_docker_image
from backend.packages.build_server.build_dockerfile import build_dockerfile


async def build_server(server, db):
    await build_dockerfile(server)
    print("Dockerfile build successful")
    image_name = await build_docker_image(server)

    return {"image_name": image_name}
