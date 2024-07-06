"""
models.py

@Author: Ethan Brown

Database models for the Fourdrinier project

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from sqlalchemy import Table, Boolean, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.session import Base


# Association table for many-to-many relationship between Playsets and Servers
playset_server_association = Table(
    "playsets_servers",
    Base.metadata,
    Column("playset_id", String, ForeignKey("playset.id")),
    Column("server_id", String, ForeignKey("server.id")),
)


class User(Base):
    __tablename__ = "user"
    username = Column(String, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    refresh_token = Column(String, default=None)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    servers = relationship("Server", back_populates="owner")
    playsets = relationship("Playset", back_populates="owner")


class Server(Base):
    __tablename__ = "server"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, default="My Server")
    loader = Column(String, nullable=False)
    game_version = Column(String, nullable=False)
    builder = Column(String, nullable=False, default="docker")
    owner_username = Column(String, ForeignKey("user.username"))
    owner = relationship("User", back_populates="servers")
    is_private = Column(Boolean, default=False)
    playsets = relationship(
        "Playset", secondary=playset_server_association, back_populates="servers"
    )


class Playset(Base):
    __tablename__ = "playset"
    id = Column(String, primary_key=True, index=True)
    name = Column(
        String,
        index=True,
        nullable=False,
        default="My Playset",
    )
    description = Column(String, default="")
    servers = relationship(
        "Server", secondary=playset_server_association, back_populates="playsets"
    )
    owner_username = Column(String, ForeignKey("user.username"))
    owner = relationship("User", back_populates="playsets")
    is_private = Column(Boolean, default=False)
