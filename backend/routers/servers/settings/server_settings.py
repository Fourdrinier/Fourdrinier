from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database import get_db
from backend.models import Server

# Import server routers

server_settings_router = APIRouter()


@server_settings_router.get("/")
async def get_server_settings(server_id: str, db: AsyncSession = Depends(get_db)):
    server = await db.get(Server, server_id, options=[selectinload(Server.settings)])
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    return server.settings
