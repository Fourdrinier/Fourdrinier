from typing import List, Any

from pydantic import BaseModel, Field


class PlaysetCreateSchema(BaseModel):
    name: str = "My Playlist"  # Default name if not otherwise defined
    mods: List[Any] = []  # Default to an empty list


class AddModToPlaysetSchema(BaseModel):
    mod_id: str


class RenamePlaysetSchema(BaseModel):
    name: str


class ServerCreateSchema(BaseModel):
    name: str = Field(default="My Server", example='Vanilla+ Server')
    loader: str = Field(..., pattern='^(paper|fabric)$', example='paper')
    game_version: str = Field(..., pattern=r'^\d+\.\d+\.\d+$', example='1.16.5')
