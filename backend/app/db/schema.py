"""
schema.py

@Author: Ethan Brown

Database schema for the Fourdrinier project

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from pydantic import BaseModel, Field
from typing import Optional


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


class UserCreate(BaseModel):
    username: str = Field(
        default="user",
        title="Username",
        description="The username of the user",
        example="user",
    )
    password: str = Field(
        default="password",
        title="Password",
        description="The password of the user",
        example="password",
    )
    email: Optional[str] = Field(
        None,
        title="Email",
        description="The email of the user",
        example="example@example.com",
    )
    registration_token: Optional[str] = Field(
        None,
        title="Registration Token",
        description="Registration token for first time setup",
    )
