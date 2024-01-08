from typing import List, Any

from pydantic import BaseModel, Field


class PlaysetCreateSchema(BaseModel):
    name: str = "My Playset"  # Default name if not otherwise defined
    mods: List[Any] = []  # Default to an empty list


class ModSchema(BaseModel):
    mod_id: str


class AddModsToPlaysetSchema(BaseModel):
    mods: List[ModSchema]


class AddCollectionToPlaysetSchema(BaseModel):
    collection_id: str


class RenamePlaysetSchema(BaseModel):
    name: str


class ServerCreateSchema(BaseModel):
    name: str = Field(default="My Server", example="Vanilla+ Server")
    loader: str = Field(..., pattern="^(paper|fabric)$", example="paper")
    game_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$", example="1.16.5")


class AddPlaysetToServerSchema(BaseModel):
    playset_id: str = Field(..., pattern=r"^[a-zA-Z0-9]{8}$", example="abcd1234")
