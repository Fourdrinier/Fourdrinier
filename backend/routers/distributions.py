"""
routers/distributions.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 28 DEC 23

Endpoints allowing for interaction with hosted files
"""
from fastapi import APIRouter, HTTPException

from backend.packages.paper.list_builds import list_builds, InvalidVersionException

router = APIRouter()


@router.get("/paper/builds/{version}")
async def list_paper_distributions(version: str):
    try:
        builds = list_builds(version)
    except InvalidVersionException as e:
        raise HTTPException(status_code=404, detail=str(e))

    return builds
