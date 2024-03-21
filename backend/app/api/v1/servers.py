"""
servers.py

@Author: Ethan Brown - ethan@ewbrowntech.com

All endpoints for servers

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the PyTube-API project and is released under
the MIT License. See the LICENSE file for more details.
"""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models import Server

# Create a new FastAPI router
router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)


@router.get("/", status_code=200)
async def list_servers(db: AsyncSession = Depends(get_db)):
    """
    List all servers
    """
    result = await db.execute(select(Server))
    servers = result.scalars().all()
    return servers
