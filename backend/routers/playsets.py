"""
routers/playsets.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 2 JAN 23

Endpoints allowing for interaction with user playsets
"""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models import Playset

router = APIRouter()


@router.get("/")
async def list_playsets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Playset))
    playsets = result.scalars().all()
    return playsets
