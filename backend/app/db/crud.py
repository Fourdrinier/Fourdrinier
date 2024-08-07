"""
crud.py

@Author: Ethan Brown - ethan@ewbrowntech.com

CRUD operations for servers

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from typing import Tuple

from sqlalchemy import Select, select
from sqlalchemy import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.db.generate_id import generate_id
from backend.app.db.models import Server
from backend.app.db.models import User
from backend.app.db.models import Playset
from backend.app.db.schema import ServerCreate


async def get_servers(db: AsyncSession) -> list[Server]:
    """
    Get all servers
    """
    result: Result[Tuple[Server]] = await db.execute(select(Server))
    servers: list[Server] = list(result.scalars().all())
    return servers


async def create_server(
    db: AsyncSession,
    server_input: ServerCreate,
    user: User,
) -> Server:
    """
    Create a new server
    """
    # Eagerly load in the user's servers
    user: User = await get_user(db, str(user.username))

    # Create the new server
    new_server = Server(**server_input.model_dump(), id=generate_id())

    # Commit the new server to the database
    try:
        user.servers.append(new_server)
        await db.commit()
        await db.refresh(new_server)
    except Exception as e:
        await db.rollback()
        raise e

    return new_server


async def list_users(db: AsyncSession) -> list[User]:
    """
    List all users
    """
    result: Result[Tuple[User]] = await db.execute(select(User))
    users: list[User] = list(result.scalars().all())
    return users


async def get_user(db: AsyncSession, username: str) -> User:
    """
    Get a user by username
    """
    result: Result[Tuple[User]] = await db.execute(
        select(User).options(selectinload(User.servers)).filter_by(username=username)
    )
    user: User | None = result.scalars().first()
    if user is None:
        raise NoResultFound("User not found")
    return user


async def create_user(
    db: AsyncSession,
    username: str,
    hashed_password: str,
    email: str | None = None,
    is_superuser: bool = False,
) -> User:
    """
    Create a new user
    """
    # Create the user
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_superuser=is_superuser,
    )

    # Commit the new user to the database
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except Exception as e:
        await db.rollback()
        raise e

    return user


async def list_playsets(db: AsyncSession) -> list[Playset]:
    """
    List all playsets
    """
    result: Result[Tuple[Playset]] = await db.execute(select(Playset))
    playsets: list[Playset] = list(result.scalars().all())
    return playsets


async def list_playsets_by_user(db: AsyncSession, user: User) -> list[Playset]:
    """
    List all playsets by a user
    """
    stmt = select(Playset)

    # If the user is not a superuser, filter the playsets
    if not user.is_superuser:  # type: ignore
        stmt: Select[Tuple[Playset]] = stmt.where(
            (Playset.owner_username == user.username) | (Playset.is_private.is_(False))
        )

    # Get the applicable playsets
    result: Result[Tuple[Playset]] = await db.execute(stmt)
    playsets: list[Playset] = list(result.scalars().all())

    return playsets
