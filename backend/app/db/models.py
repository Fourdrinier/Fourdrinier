"""
models.py

@Author: Ethan Brown

Database models for the Fourdrinier project

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class User(Base):
    __tablename__ = "user"
    username = Column(String, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    refresh_token = Column(String, default=None)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    servers = relationship("Server", back_populates="owner")


class Server(Base):
    __tablename__ = "server"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    loader = Column(String, nullable=False)
    game_version = Column(String, nullable=False)
    builder = Column(String, nullable=False, default="docker")
    owner_username = Column(String, ForeignKey("user.username"))
    owner = relationship("User", back_populates="servers")
