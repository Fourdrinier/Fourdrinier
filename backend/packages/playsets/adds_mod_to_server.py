import json
import time

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database import generate_unique_id
from backend.models import Server, ServerMod
from backend.packages.modrinth.projects import get_projects
from backend.packages.modrinth.versions import get_latest_compatible_version


async def add_projects_to_server(server_id, project_ids, db: AsyncSession):
    stmt = (
        select(Server).options(selectinload(Server.server_mods)).filter_by(id=server_id)
    )
    result = await db.execute(stmt)
    server = result.scalar_one()
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")

    # Get projects
    projects = await get_projects(project_ids)

    # Get the list of projects that are not yet added to the server
    existing_project_ids = [server_mod.project_id for server_mod in server.server_mods]
    new_projects = [
        project for project in projects if project["id"] not in existing_project_ids
    ]

    # Add the new projects to the server
    for project in new_projects:
        version = await get_latest_compatible_version(
            project["id"], server.loader, server.game_version
        )
        supported_game_versions = [
            game_version for game_version in version["game_versions"]
        ]
        server_mod = ServerMod(
            id=generate_unique_id(),
            title=project["title"],
            project_id=project["id"],
            project_type=project["project_type"],
            version_id=version["id"],
            version_name=version["name"],
            supported_versions=json.dumps({"game_versions": supported_game_versions}),
            url=version["files"][0]["url"],
        )
        server.server_mods.append(server_mod)
        time.sleep(0.2)

    await db.commit()
    await db.refresh(server)

    return server
