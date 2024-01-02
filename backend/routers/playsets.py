"""
routers/playsets.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 2 JAN 23

Endpoints allowing for interaction with user playsets
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db, generate_unique_id
from backend.models import Playset
from backend.schema import PlaysetCreateSchema

router = APIRouter()


@router.get("/")
async def list_playsets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Playset))
    playsets = result.scalars().all()
    return playsets


@router.post("/")
async def create_playset(
    playset_data: PlaysetCreateSchema, db: AsyncSession = Depends(get_db)
):
    new_playset = Playset(id=generate_unique_id(), **playset_data.dict())

    # Add to the database
    db.add(new_playset)
    await db.commit()
    await db.refresh(new_playset)

    return new_playset


@router.get("/{playset_id}")
async def show_playset(playset_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Playset).where(Playset.id == playset_id))
    playset = result.scalars().first()
    if playset is None:
        raise HTTPException(status_code=404, detail="Playset not found")
    return playset
