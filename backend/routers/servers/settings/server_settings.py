from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database import get_db
from backend.models import Server
from backend.schema import UpdateServerSettingsSchema

# Import server routers

server_settings_router = APIRouter()


@server_settings_router.get("/")
async def get_server_settings(server_id: str, db: AsyncSession = Depends(get_db)):
    server = await db.get(Server, server_id, options=[selectinload(Server.settings)])
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    return server.settings


@server_settings_router.patch("/")
async def update_server_settings(
    server_id: str,
    settings_data: UpdateServerSettingsSchema,
    db: AsyncSession = Depends(get_db),
):
    # Get the server object by its ID
    server = await db.get(Server, server_id, options=[selectinload(Server.settings)])
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")

    # Update any fields specified in the request
    for var, value in vars(settings_data).items():
        if value is not None:
            setattr(server.settings, var, value)
    await db.commit()
    await db.refresh(server.settings)
    return server.settings
