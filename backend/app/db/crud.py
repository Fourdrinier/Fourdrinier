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
from sqlalchemy import select
from sqlalchemy import Result
from app.db.models import Server


async def get_servers(db: AsyncSession) -> Sequence[Server]:
    """
    Get all servers
    """
    result: Result[Tuple[Server]] = await db.execute(select(Server))
    servers: Sequence[Server] = result.scalars().all()
    return servers
