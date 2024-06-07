"""
servers.py

@Author: Ethan Brown - ethan@ewbrowntech.com

All endpoints for servers

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the MIT License. See the LICENSE file for more details.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.db.models import Server, User
from app.db.schema import ServerCreate, ServerResponse
from app.db.generate_id import generate_id

from app.dependencies.config.get_config import get_config
from app.dependencies.jwt.validate_user import validate_user


# Create a new FastAPI router
router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)

# Get the configuration
config = get_config()


@router.get("/", status_code=200)
async def list_servers(db: AsyncSession = Depends(get_db)):
    """
    List all servers
    """
    result = await db.execute(select(Server))
    servers = result.scalars().all()
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
