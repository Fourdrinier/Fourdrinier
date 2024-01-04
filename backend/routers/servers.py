"""
routers/distributions.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 02 JAN 24

Endpoints allowing for interaction with hosted files
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database import get_db, generate_unique_id
from backend.models import Server, Playset, ServerResponse, PlaysetResponse
from backend.packages.fabric.build_server import build_server as build_fabric_server
from backend.schema import ServerCreateSchema, AddPlaysetToServerSchema

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
    new_server = Server(id=generate_unique_id(), **server_data.model_dump())
    db.add(new_server)
    await db.commit()
    await db.refresh(new_server)
    return new_server


@router.post("/{server_id}/playset")
async def add_playset_to_server(
    server_id: str,
    playset_data: AddPlaysetToServerSchema,
    db: AsyncSession = Depends(get_db),
):
    server = await db.get(Server, server_id)
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    playset = await db.get(
        Playset, playset_data.playset_id, options=[selectinload(Playset.mods)]
    )
    if playset is None:
        raise HTTPException(status_code=404, detail="Playset not found")

    server.playset = playset
    await db.commit()
    await db.refresh(server)

    response = ServerResponse(
        id=server.id,
        name=server.name,
        game_version=server.game_version,
        loader=server.loader,
        playset=PlaysetResponse(
            id=playset.id, name=playset.name, mods=[mod.id for mod in playset.mods]
        ),
    )
    return response


@router.delete("/{server_id}/playset")
async def remove_playset_from_server(
    server_id: str, db: AsyncSession = Depends(get_db)
):
    server = await db.get(Server, server_id)
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    server.playset_id = None
    await db.commit()
    await db.refresh(server)
    return server


@router.post("/{server_id}/build")
async def build_server(server_id: str, db: AsyncSession = Depends(get_db)):
    server = await db.get(Server, server_id)
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    match server.loader:
        case "fabric":
            response = await build_fabric_server(server)

    return response
