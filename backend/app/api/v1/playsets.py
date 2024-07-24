"""
playsets.py

@Author: Ethan Brown - ethan@ewbrowntech.com

All endpoints for playsets

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from fastapi import APIRouter, Depends
import logging

from sqlalchemy.ext.asyncio import AsyncSession

import backend.app.db.crud as crud
from backend.app.db.session import get_db
from backend.app.db.models import Playset, User
from backend.app.db.schema import PlaysetResponse

from backend.app.dependencies.core.auth.validate_user import validate_user


# Create a new FastAPI router
router = APIRouter()

# Configure logging
logger: logging.Logger = logging.getLogger(__name__)


@router.get("/", status_code=200, response_model=list[PlaysetResponse])
async def list_playsets(
    db: AsyncSession = Depends(get_db), user: User = Depends(validate_user)
) -> list[PlaysetResponse]:
    """
    List all playsets
    """
    playsets: list[Playset] = await crud.list_playsets_by_user(db, user)

    return [PlaysetResponse.model_validate(playset.__dict__) for playset in playsets]
