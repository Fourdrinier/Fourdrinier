"""
routers/distributions.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 02 JAN 24

Endpoints allowing for interaction with hosted files
"""
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db, generate_unique_id
from backend.models import Server

router = APIRouter()


@router.get("/")
async def list_servers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Server))
    servers = result.scalars().all()
    return servers