import docker
from fastapi import HTTPException

from backend.packages.storage.get_server_directory import get_server_directory


async def build_docker_image(server):
    server_directory = await get_server_directory(server.id)
    image_name = "fabric-" + server.id
    # Create a Docker client
    with docker.APIClient(base_url="unix://var/run/docker.sock") as low_level_client:
        # Stream the build output
        response = low_level_client.build(
            path=server_directory, tag=image_name, decode=True
        )

    # Compile the build log
    build_log = []
    for item in response:
        message = item.get("stream") or item.get("aux")
        if message and message != "\n":
            build_log.append(message)

    # If the build failed, remove the image. Otherwise, return the image name
    if len(build_log) > 0 and "Successfully built" in build_log[-2]:
        return image_name
    else:
        with docker.from_env() as client:
            client.images.remove(image=image_name)
        raise HTTPException(status_code=500, detail="Failed to build Docker image")
