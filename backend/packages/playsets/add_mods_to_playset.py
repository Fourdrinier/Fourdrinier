import httpx
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Mod

router = APIRouter()


async def add_mods_to_playset(mods, playset, db: AsyncSession):
    for project_id in mods:
        # Check if Mod exists in the Modrinth API
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.modrinth.com/v2/project/{project_id}"
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=404,
                    detail=f"Project {project_id} not found in Modrinth API",
                )
            else:
                title = response.json().get("title")

        # Check if the mod exists in the database
        mod_entry = await db.get(Mod, project_id)
        if mod_entry is None:
            mod_entry = Mod(id=project_id, title=title)
            db.add(mod_entry)
            await db.commit()
            await db.refresh(mod_entry)

        if mod_entry not in playset.mods:
            playset.mods.append(mod_entry)
            await db.commit()
            await db.refresh(playset)
        else:
            pass

    return playset
