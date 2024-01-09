from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import Mod, Playset
from backend.packages.modrinth.projects import get_projects

router = APIRouter()


async def add_mods_to_playset(mods, playset_id, db: AsyncSession, verify=True):
    stmt = select(Playset).options(selectinload(Playset.mods)).filter_by(id=playset_id)
    result = await db.execute(stmt)
    playset = result.scalar_one()
    if playset is None:
        raise HTTPException(status_code=404, detail="Playset not found")

    mods = await get_projects(mods)

    for project in mods:
        # Check if the mod exists in the database
        mod_entry = await db.get(Mod, project["id"])
        if mod_entry is None:
            mod_entry = Mod(id=project["id"], title=project["title"])
            db.add(mod_entry)
            await db.commit()
            await db.refresh(mod_entry)

        if mod_entry not in playset.mods:
            playset.mods.append(mod_entry)
        else:
            pass
    await db.commit()
    await db.refresh(playset)

    return playset
