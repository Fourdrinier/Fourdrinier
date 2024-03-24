"""
schema.py

@Author: Ethan Brown

Database schema for the Fourdrinier project

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from pydantic import BaseModel, Field


class ServerCreate(BaseModel):
    name: str = Field(
        default="My Server",
        title="Server Name",
        description="The name of the server",
        example="Vanilla+ Server",
    )
    loader: str = Field(
        ..., title="Loader", pattern="^(paper|fabric)$", example="paper"
    )
    game_version: str = Field(
        ..., pattern=r"^\d+\.\d+\.\d+$", title="Game Version", example="1.17.1"
    )
