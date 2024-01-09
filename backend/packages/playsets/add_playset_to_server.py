from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import Playset
from backend.models import Server
from backend.packages.modrinth.dependencies import get_dependencies
from backend.packages.playsets.adds_mod_to_server import add_projects_to_server


async def add_playset_to_server(server_id, playset_id, db: AsyncSession):
    playset = await db.get(Playset, playset_id, options=[selectinload(Playset.mods)])
    if playset is None:
        raise HTTPException(status_code=404, detail="Playset not found")
    project_ids = [mod.id for mod in playset.mods]

    await add_projects_to_server(server_id, project_ids, db)

    # Refresh the server object
    stmt = (
        select(Server).options(selectinload(Server.server_mods)).filter_by(id=server_id)
    )
    result = await db.execute(stmt)
    server = result.scalar_one()

    # Get the version ID's of all projects on the server
    version_ids = []
    for mod in server.server_mods:
        version_ids.append(mod.version_id)

    # Add the dependencies to the mod list
    required_dependencies, optional_dependencies = await get_dependencies(version_ids)
    await add_projects_to_server(
        server_id, required_dependencies, db, role="required_dependency"
    )
    await add_projects_to_server(
        server_id, optional_dependencies, db, role="optional_dependency"
    )
    return server
