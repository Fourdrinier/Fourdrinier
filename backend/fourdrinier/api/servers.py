"""
servers.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Endpoints for interacting with server objects.

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from backend.fourdrinier.db import crud
from backend.fourdrinier.db.models import Server
from backend.fourdrinier.db.schema import ServerCreate
from backend.fourdrinier.db.schema import ServerResponse
from backend.fourdrinier.db.session import get_db


router = APIRouter()


@router.post("/", status_code=201, response_model=ServerResponse)
async def create_server(server_input: ServerCreate, db: AsyncSession = Depends(get_db)) -> Server:
    """
    Create a new server
    """
    server: Server = await crud.create_server(db, server_input)
    return server


@router.get("/", status_code=200, response_model=list[ServerResponse])
async def list_servers(db: AsyncSession = Depends(get_db)) -> list[Server]:
    """
    List all servers
    """
    servers: list[Server] = await crud.list_servers(db)
    return servers


@router.get("/{server_id}", status_code=200, response_model=ServerResponse)
async def get_server(server_id: str, db: AsyncSession = Depends(get_db)) -> Server:
    """
    Get a server by ID
    """
    try:
        server: Server = await crud.get_server(db, server_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Server not found")
    return server
