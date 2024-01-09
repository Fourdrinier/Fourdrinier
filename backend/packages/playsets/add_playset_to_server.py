from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import Playset
from backend.packages.playsets.adds_mod_to_server import add_projects_to_server


async def add_playset_to_server(server_id, playset_id, db: AsyncSession):
    playset = await db.get(Playset, playset_id, options=[selectinload(Playset.mods)])
    if playset is None:
        raise HTTPException(status_code=404, detail="Playset not found")
    project_ids = [mod.id for mod in playset.mods]

    server = await add_projects_to_server(server_id, project_ids, db)
    return server
