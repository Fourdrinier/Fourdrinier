"""
crud.py

@Author: Ethan Brown - ethan@ewbrowntech.com

CRUD operations for servers

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from typing import Sequence, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select
from sqlalchemy import Result
from sqlalchemy.orm import selectinload

from backend.app.db.generate_id import generate_id
from backend.app.db.models import Server
from backend.app.db.models import User
from backend.app.db.schema import ServerCreate


async def crud_get_servers(db: AsyncSession) -> Sequence[Server]:
    """
    Get all servers
    """
    result: Result[Tuple[Server]] = await db.execute(select(Server))
    servers: Sequence[Server] = result.scalars().all()
    return servers


async def crud_create_server(
    db: AsyncSession,
    server_input: ServerCreate,
    user: User,
) -> Server:
    """
    Create a new server
    """
    new_server = Server(**server_input.model_dump(), id=generate_id())

    # Eagler load in the user's servers
    stmt: Select[Tuple[User]] = (
        select(User)
        .options(selectinload(User.servers))
        .filter_by(username=user.username)
    )
    result: Result[Tuple[User]] = await db.execute(stmt)
    user: User = result.scalars().first()
    if user is None:
        raise ValueError("User not found")
    user.servers.append(new_server)

    return new_server
