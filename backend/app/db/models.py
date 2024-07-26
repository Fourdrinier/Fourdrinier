"""
models.py

@Author: Ethan Brown

Database models for the Fourdrinier project

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from typing import Optional

from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.app.db.session import Base


# Association table for many-to-many relationship between Playsets and Servers
playset_server_association = Table(
    "playsets_servers",
    Base.metadata,
    Column("playset_id", String, ForeignKey("playset.id")),
    Column("server_id", String, ForeignKey("server.id")),
)


class User(Base):
    __tablename__: str = "user"
    username: Mapped[str] = mapped_column(primary_key=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    refresh_token: Mapped[Optional[str]] = mapped_column(default=None)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    servers = relationship("Server", back_populates="owner")
    playsets = relationship("Playset", back_populates="owner")


class Server(Base):
    __tablename__: str = "server"
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, default="My Server")
    loader: Mapped[str]
    game_version: Mapped[str]
    builder: Mapped[str] = mapped_column(default="docker")
    owner_username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    owner = relationship("User", back_populates="servers")
    is_private: Mapped[bool] = mapped_column(default=False)
    playsets = relationship(
        "Playset", secondary=playset_server_association, back_populates="servers"
    )
    settings = relationship(
        "Settings", back_populates="server", uselist=False, cascade="all, delete-orphan"
    )


class Playset(Base):
    __tablename__: str = "playset"
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, default="My Playset")
    description: Mapped[str] = mapped_column(default="")
    servers = relationship(
        "Server", secondary=playset_server_association, back_populates="playsets"
    )
    owner_username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    owner = relationship("User", back_populates="playsets")
    is_private: Mapped[bool] = mapped_column(default=False)


class Settings(Base):
    __tablename__: str = "settings"
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    server_id: Mapped[str] = mapped_column(ForeignKey("server.id"), unique=True)
    server = relationship("Server", back_populates="settings")

    # Server settings
    allocated_memory: Mapped[int] = mapped_column(default=2048)
    level_seed: Mapped[str] = mapped_column(default="")
    motd: Mapped[str] = mapped_column(default="A Fourdrinier Server")
    view_distance: Mapped[int] = mapped_column(default=16)
