"""
playsets.py

@Author: Ethan Brown - ethan@ewbrowntech.com

All endpoints for playsets

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
from app.db.models import Playset, User
from app.db.schema import ServerCreate, ServerResponse
from app.db.generate_id import generate_id

from app.dependencies.config.get_config import get_config
from app.dependencies.jwt.validate_user import validate_user


# Create a new FastAPI router
router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)


@router.get("/", status_code=200)
async def list_playsets(db: AsyncSession = Depends(get_db)):
    """
    List all playsets
    """
    result = await db.execute(select(Playset))
    servers = result.scalars().all()
    return servers
