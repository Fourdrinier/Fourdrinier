"""
routers/playsets.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 3 JAN 23

Endpoints allowing for interaction with user playsets
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database import get_db, generate_unique_id
from backend.models import Playset, Mod, PlaysetResponse
from backend.packages.modrinth.collections import get_collection
from backend.packages.playsets.add_mods_to_playset import add_mods_to_playset
from backend.schema import (
    PlaysetCreateSchema,
    AddModsToPlaysetSchema,
    AddCollectionToPlaysetSchema,
    RenamePlaysetSchema,
)

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
    playset = await db.get(Playset, playset_id, options=[selectinload(Playset.mods)])
    if playset is None:
        raise HTTPException(status_code=404, detail="Playset not found")
    response = PlaysetResponse(
        id=playset.id, name=playset.name, mods=[mod.id for mod in playset.mods]
    )
    return response


@router.patch("/{playset_id}")
async def rename_playset(
    playset_id: str, new_data: RenamePlaysetSchema, db: AsyncSession = Depends(get_db)
):
    playset = await db.get(Playset, playset_id, options=[selectinload(Playset.mods)])
    if not playset:
        raise HTTPException(status_code=404, detail="Playset not found")

    playset.name = new_data.name
    db.add(playset)
    await db.commit()
    await db.refresh(playset)
    response = PlaysetResponse(
        id=playset.id, name=playset.name, mods=[mod.id for mod in playset.mods]
    )
    return response


@router.delete("/{playset_id}")
async def delete_playset(playset_id: str, db: AsyncSession = Depends(get_db)):
    playset = await db.get(Playset, playset_id)
    if not playset:
        raise HTTPException(status_code=404, detail="Playset not found")
    await db.delete(playset)
    await db.commit()

    # Remove any orphaned mods (that are no longer associated with any playsets)
    orphaned_mods = (
        (await db.execute(select(Mod).where(~Mod.playsets.any()))).scalars().all()
    )
    for mod in orphaned_mods:
        await db.delete(mod)
    await db.commit()

    return {"message": "Playset deleted"}


@router.post("/{playset_id}/mods")
async def add_mod_to_playset(
    playset_id: str,
    mod_data: AddModsToPlaysetSchema,
    db: AsyncSession = Depends(get_db),
):
    playset = await db.get(Playset, playset_id, options=[selectinload(Playset.mods)])
    if playset is None:
        raise HTTPException(status_code=404, detail="Playset not found")
    mods = [
        mod.mod_id for mod in mod_data.mods
    ]  # Translate the mod list into one add_mods_to_playset() can read
    playset = await add_mods_to_playset(mods, playset, db)

    response = PlaysetResponse(
        id=playset.id, name=playset.name, mods=[mod.id for mod in playset.mods]
    )
    return response


@router.post("/{playset_id}/collection")
async def add_mods_to_playset_via_collection(
    playset_id: str,
    collection: AddCollectionToPlaysetSchema,
    db: AsyncSession = Depends(get_db),
):
    playset = await db.get(Playset, playset_id, options=[selectinload(Playset.mods)])
    if playset is None:
        raise HTTPException(status_code=404, detail="Playset not found")

    collection = await get_collection(collection.collection_id)
    playset = await add_mods_to_playset(collection["projects"], playset, db)

    response = PlaysetResponse(
        id=playset.id, name=playset.name, mods=[mod.id for mod in playset.mods]
    )
    return response


@router.delete("/{playset_id}/mods/{mod_id}")
async def remove_mod_from_playset(
    playset_id: str, mod_id: str, db: AsyncSession = Depends(get_db)
):
    playset = await db.get(Playset, playset_id, options=[selectinload(Playset.mods)])
    if not playset:
        raise HTTPException(status_code=404, detail="Playset not found")

    mod = await db.get(Mod, mod_id)
    if not mod:
        raise HTTPException(status_code=404, detail="Mod not found")

    if mod in playset.mods:
        playset.mods.remove(mod)
        await db.commit()
    else:
        pass

    response = PlaysetResponse(
        id=playset.id, name=playset.name, mods=[mod.id for mod in playset.mods]
    )
    return response
