from typing import List, Any

from pydantic import BaseModel


class PlaysetCreateSchema(BaseModel):
    name: str = "My Playlist"  # Default name if not otherwise defined
    mods: List[Any] = []  # Default to an empty list


class AddModToPlaysetSchema(BaseModel):
    mod_id: str


class RenamePlaysetSchema(BaseModel):
    name: str