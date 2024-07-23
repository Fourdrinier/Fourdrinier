"""
servers.py

@Author: Ethan Brown - ethan@ewbrowntech.com

All endpoints for servers

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import logging
from typing import Tuple, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload
from typing import Sequence

from backend.app.db.models import Server, User
from backend.app.db.schema import ServerCreate, ServerResponse
from backend.app.db.generate_id import generate_id

from backend.app.db.session import get_db

from backend.app.dependencies.core.config.get_config import get_config
from backend.app.dependencies.core.auth.validate_user import validate_user

import backend.app.db.crud as crud

# Create a new FastAPI router
router = APIRouter()

# Configure logging
logger: logging.Logger = logging.getLogger(__name__)

# Get the configuration
config: Any = get_config()


@router.get("/", status_code=200, response_model=list[ServerResponse])
async def list_servers(db: AsyncSession = Depends(get_db)) -> list[Server]:
    """
    List all servers
    """
    servers: list[Server] = await crud.get_servers(db)
    return servers


@router.post("/", status_code=201, response_model=ServerResponse)
async def create_server(
    server_input: ServerCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(validate_user),
) -> Server:
    """
    Create a new server
    """

    # Validate the loader
    if server_input.loader not in config["loaders"]:
        raise HTTPException(status_code=400, detail="Invalid loader")

    # Validate the game version
    if server_input.game_version not in config["supported_versions"]:
        raise HTTPException(status_code=400, detail="Unsupported game version")

    # Commit the new server to the database
    new_server: Server = await crud.create_server(db, server_input, user)

    return new_server


@router.get("/{server_id}", status_code=200, response_model=ServerResponse)
async def get_server(server_id: str, db: AsyncSession = Depends(get_db)) -> Server:
    """
    Get a server by ID
    """
    result: Result[Tuple[Server]] = await db.execute(
        select(Server).filter_by(id=server_id)
    )
    server: Server | None = result.scalars().first()
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    return server
