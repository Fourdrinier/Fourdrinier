"""
routers/distributions.py

@Author - Ethan Brown - ewbrowntech@gmail.com

Endpoints allowing for interaction with hosted files
"""

import docker
from docker.errors import NotFound
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database import get_db, generate_unique_id
from backend.models import (
    Server,
    ServerSettings,
    Playset,
    ServerResponse,
    ServerModResponse,
)
from backend.packages.build_server.build_server import (
    build_server as build_server_image,
)
from backend.packages.fabric.run_server import run_new_container
from backend.packages.playsets.add_playset_to_server import add_playset_to_server
# Import server routers
from backend.routers.servers.settings.server_settings import server_settings_router
from backend.schema.schema import ServerCreateSchema, AddPlaysetToServerSchema

router = APIRouter()


@router.get("/")
async def list_servers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Server))
    servers = result.scalars().all()
    return servers


@router.post("/")
async def create_server(
    server_data: ServerCreateSchema, db: AsyncSession = Depends(get_db)
):
    new_server = Server(id=generate_unique_id(), name=server_data.name)
    server_data = server_data.model_dump()
    server_data.pop("name", None)  # Example of removing a non-Profile field
    new_server_settings = ServerSettings(
        id=generate_unique_id(), server=new_server, **server_data
    )

    db.add(new_server)
    db.add(new_server_settings)
    await db.commit()

    await db.refresh(new_server)
    await db.refresh(new_server_settings)

    return new_server


@router.post("/{server_id}/playset")
async def add_playset_to_server_endpoint(
    server_id: str,
    playset_data: AddPlaysetToServerSchema,
    db: AsyncSession = Depends(get_db),
):
    playset_id = playset_data.playset_id
    server = await db.get(Server, server_id, options=[selectinload(Server.settings)])
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    playset = await db.get(Playset, playset_id, options=[selectinload(Playset.mods)])
    if playset is None:
        raise HTTPException(status_code=404, detail="Playset not found")

    server = await add_playset_to_server(server_id, playset_id, db)

    result = await db.execute(
        select(Server)
        .options(selectinload(Server.server_mods))
        .filter(Server.id == server.id)
    )
    server = result.scalars().first()

    response = ServerResponse(
        id=server.id,
        name=server.name,
        game_version=server.settings.game_version,
        loader=server.settings.loader,
        projects=[
            ServerModResponse(
                id=mod.project_id,
                title=mod.title,
                version=mod.version_id,
                version_name=mod.version_name,
                role=mod.role,
            )
            for mod in server.server_mods
        ],
    )
    return response


@router.post("/{server_id}/build")
async def build_server(server_id: str, db: AsyncSession = Depends(get_db)):
    server = await db.get(
        Server,
        server_id,
        options=[selectinload(Server.server_mods), selectinload(Server.settings)],
    )
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    response = await build_server_image(server, db)
    return response


@router.post("/{server_id}/run")
async def run_server(server_id: str, db: AsyncSession = Depends(get_db)):
    server = await db.get(Server, server_id, options=[selectinload(Server.settings)])
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")

    # Check if there is an existing container for the server
    container_name = server.settings.loader + "-" + server.id
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
    except NotFound:
        return await run_new_container(server)

    # If there is already a container for the server, simply start it
    container.start()
    container.reload()

    return {"container_id": container.id}


@router.post("/{server_id}/stop")
async def stop_server(server_id: str, db: AsyncSession = Depends(get_db)):
    server = await db.get(Server, server_id)
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")

    # Get the container
    container_name = server.settings.loader + "-" + server.id
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
    except NotFound:
        return HTTPException(
            status_code=404, detail="No container found for given server"
        )

    match container.status:
        case "exited":
            return Response(
                content="Container was already exited",
                status_code=status.HTTP_202_ACCEPTED,
            )
        case "running" | "paused" | "restarting":
            container.stop()
            container.reload()
            return {"container_id": container.id, "status": container.status}
        case "dead":
            HTTPException(
                status_code=500,
                detail=f"Container {container_name} is dead. Try rebuilding the server.",
            )
        case "removing":
            HTTPException(
                status_code=500,
                detail=f"Container {container_name} is being removed. Try rebuilding the server.",
            )
        case _:
            HTTPException(
                status_code=500,
                detail=f"Unable to determine status of {container_name}. Try rebuilding the server.",
            )


router.include_router(server_settings_router, prefix="/{server_id}/settings")
