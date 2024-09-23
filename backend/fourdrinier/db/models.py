"""
models.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Models for database tables and relationships

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .session import Base


class Server(Base):
    __tablename__ = "servers"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, default="My Server")
    loader: Mapped[str]
    game_version: Mapped[str]
