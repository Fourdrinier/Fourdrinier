"""
playsets.py

@Author: Ethan Brown - ethan@ewbrowntech.com

All endpoints for playsets

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.app.db.session import get_db
from backend.app.db.models import Playset, User
from backend.app.db.schema import PlaysetResponse
from backend.app.db.generate_id import generate_id

from backend.app.dependencies.config.get_config import get_config
from backend.app.dependencies.jwt.validate_user import validate_user


# Create a new FastAPI router
router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)


@router.get("/", status_code=200, response_model=list[PlaysetResponse])
async def list_playsets(
    db: AsyncSession = Depends(get_db), user: User = Depends(validate_user)
):
    """
    List all playsets
    """
    # If the user is a superuser, get all playsets
    stmt = select(Playset)

    # If the user is not a superuser, filter the playsets
    if not user.is_superuser:
        stmt = stmt.where(
            (Playset.owner_username == user.username) | (Playset.is_private == False)
        )

    # Get the applicable playsets
    result = await db.execute(stmt)
    playsets = result.scalars().all()

    return playsets
