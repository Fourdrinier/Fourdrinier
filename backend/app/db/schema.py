"""
schema.py

@Author: Ethan Brown

Database schema for the Fourdrinier project

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ServerCreate(BaseModel):
    name: str = Field(
        default="My Server",
        title="Server Name",
        description="The name of the server",
        json_schema_extra={"examples": ["My Server"]},
    )
    loader: str = Field(
        default="paper",
        title="Loader",
        json_schema_extra={"examples": ["paper"]},
    )
    game_version: str = Field(
        ...,
        pattern=r"^\d+\.\d+\.\d+$",
        title="Game Version",
        json_schema_extra={"examples": ["1.17.1"]},
    )
    builder: Optional[str] = Field(
        default="docker",
        title="Builder",
        description="The builder to use",
        json_schema_extra={"examples": ["docker"]},
    )


class ServerResponse(BaseModel):
    id: str
    name: str
    loader: str
    game_version: str


class UserCreate(BaseModel):
    username: str = Field(
        default="user",
        title="Username",
        description="The username of the user",
        json_schema_extra={"examples": ["user"]},
    )
    password: str = Field(
        default="password",
        title="Password",
        description="The password of the user",
        json_schema_extra={"examples": ["password"]},
    )
    email: Optional[str] = Field(
        None,
        title="Email",
        description="The email of the user",
        json_schema_extra={"examples": ["example@example.com"]},
    )
    registration_token: Optional[str] = Field(
        None,
        title="Registration Token",
        description="Registration token for first time setup",
    )


class UserLogin(BaseModel):
    username: str = Field(
        title="Username",
        description="The username of the user",
        json_schema_extra={"examples": ["user"]},
    )
    password: str = Field(
        title="Password",
        description="The password of the user",
        json_schema_extra={"examples": ["password"]},
    )


class PlaysetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    description: str
    owner_username: str
    is_private: bool


class RegistrationResponse(BaseModel):
    username: str
    is_superuser: bool


class LoginResponse(BaseModel):
    username: str
    jwt: str
    refresh_token: str
