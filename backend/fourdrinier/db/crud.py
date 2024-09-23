"""
crud.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Methods for creating, reading, updating, and deleting data in the database.

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import uuid
from typing import Sequence
from typing import Tuple

from sqlalchemy import Result
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from backend.fourdrinier.db.models import Server
from backend.fourdrinier.db.schema import ServerCreate


async def create_server(db: AsyncSession, server: ServerCreate) -> Server:
    """
    Create a new server object in the database.
    """
    new_server = Server(**server.model_dump())
    new_server.id = str(uuid.uuid4())
    try:
        db.add(new_server)
        await db.commit()
        await db.refresh(new_server)
    except Exception as e:
        await db.rollback()
        raise e
    return new_server


async def get_server(db: AsyncSession, server_id: str) -> Server:
    """
    Retrieve a server object from the database.
    """
    server: Server | None = await db.get(Server, server_id)
    if server is None:
        raise NoResultFound
    return server


async def list_servers(db: AsyncSession) -> list[Server]:
    """
    Retrieve all server objects from the database.
    """
    result: Result[Tuple[Server]] = await db.execute(select(Server))
    servers: Sequence[Server] = result.scalars().all()
    return list(servers)
