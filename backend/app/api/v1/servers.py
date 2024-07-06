"""
servers.py

@Author: Ethan Brown - ethan@ewbrowntech.com

All endpoints for servers

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import logging
from typing import Tuple
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload
from typing import Sequence

from backend.app.db.session import get_db
from backend.app.db.models import Server, User
from backend.app.db.schema import ServerCreate, ServerResponse
from backend.app.db.generate_id import generate_id

from backend.app.dependencies.config.get_config import get_config
from backend.app.dependencies.jwt.validate_user import validate_user

from backend.app.db.crud import get_servers

# Create a new FastAPI router
router = APIRouter()

# Configure logging
logger: logging.Logger = logging.getLogger(__name__)

# Get the configuration
config = get_config()


@router.get("/", status_code=200)
async def list_servers(db: AsyncSession = Depends(get_db)):
    """
    List all servers
    """
    servers: Sequence[Server] = await get_servers(db)
    return servers


@router.post("/", status_code=201, response_model=ServerResponse)
async def create_server(
    server: ServerCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(validate_user),
):
    """
    Create a new server
    """
    # Create a new server object
    new_server = Server(**server.model_dump(), id=generate_id())

    # Validate the loader
    if new_server.loader not in config["loaders"]:
        raise HTTPException(status_code=400, detail="Invalid loader")

    # Validate the game version
    if new_server.game_version not in config["supported_versions"]:
        raise HTTPException(status_code=400, detail="Unsupported game version")

    # Get the user object and add the server to the user's list of servers
    stmt = (
        select(User)
        .options(selectinload(User.servers))
        .filter_by(username=user.username)
    )
    result = await db.execute(stmt)
    user = result.scalars().first()
    user.servers.append(new_server)

    # Save the server to the database
    await db.commit()
    await db.refresh(new_server)

    return new_server


@router.get("/{server_id}", status_code=200)
async def get_server(server_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get a server by ID
    """
    result = await db.execute(select(Server).filter_by(id=server_id))
    server = result.scalars().first()
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    return server
