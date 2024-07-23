"""
users.py

@Author: Ethan Brown - ethan@ewbrowntech.com

All endpoints for users

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from fastapi import APIRouter, Depends, HTTPException
import logging
import os
import secrets

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

import backend.app.db.crud as crud
from backend.app.db.models import User
from backend.app.db.schema import (
    UserCreate,
    UserLogin,
    RegistrationResponse,
    LoginResponse,
)
from backend.app.db.session import get_db

from backend.app.dependencies.core.auth.generate_jwt import generate_jwt
from backend.app.dependencies.core.auth.verify_password import verify_password
from backend.app.dependencies.core.auth.get_password_hash import get_password_hash


# Create a new FastAPI router
router = APIRouter()

# Configure logging
logger: logging.Logger = logging.getLogger(__name__)


@router.post("/superuser/", status_code=201, response_model=RegistrationResponse)
async def register_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> RegistrationResponse:
    """
    Register a new superuser
    """
    # Check if there are already users in the database. If so, restrict endpoint.
    users: list[User] = await crud.list_users(db)
    if len(users) > 0:
        raise HTTPException(status_code=404)

    # Ensure that the user provided a valid registration token
    if not user.registration_token:
        raise HTTPException(
            status_code=400,
            detail="Superuser registration requires a registration token",
        )
    if user.registration_token != os.getenv("REGISTRATION_TOKEN"):
        raise HTTPException(status_code=400, detail="Invalid registration token")

    # Hash the password
    hashed_password: str = await get_password_hash(user.password)

    # Create the user
    user: User = await crud.create_user(
        db=db,
        username=user.username,
        hashed_password=hashed_password,
        email=user.email,
        is_superuser=True,
    )

    return RegistrationResponse(
        username=str(user.username), is_superuser=bool(user.is_superuser)
    )


@router.post("/login", status_code=200, response_model=LoginResponse)
async def login(
    user_input: UserLogin, db: AsyncSession = Depends(get_db)
) -> LoginResponse:
    """
    Log in a user
    """
    # Get the user from the database
    try:
        user: User = await crud.get_user(db, user_input.username)
    except NoResultFound:
        raise HTTPException(
            status_code=401, detail="The provided credentials were incorrect"
        )

    # Check the password
    if not await verify_password(user_input.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=401, detail="The provided credentials were incorrect"
        )

    # Create a JWT
    jwt: str = generate_jwt(username=str(user.username))

    # Create a refresh token
    refresh_token: str = secrets.token_hex(32)
    user.refresh_token = refresh_token  # type: ignore
    await db.commit()
    await db.refresh(user)

    return LoginResponse(
        username=str(user.username), jwt=jwt, refresh_token=refresh_token
    )


@router.post("/refresh", status_code=200, response_model=LoginResponse)
async def refresh_token(
    refresh_token: str, client_id: str, db: AsyncSession = Depends(get_db)
) -> LoginResponse:
    """
    Refresh a JWT
    """
    # Get the requested user from the database
    try:
        user: User = await crud.get_user(db, client_id)
    except NoResultFound:
        raise HTTPException(
            status_code=401, detail="The provided credentials were incorrect"
        )

    # Ensure that the refresh token is valid
    if str(user.refresh_token) != refresh_token:
        raise HTTPException(
            status_code=401, detail="The provided credentials were incorrect"
        )

    # Create a new JWT
    jwt: str = generate_jwt(username=str(user.username))

    # Create a new refresh token
    new_refresh_token: str = secrets.token_hex(32)

    # Commit the new user to the database
    try:
        user.refresh_token = new_refresh_token  # type: ignore
        await db.commit()
        await db.refresh(user)
    except Exception as e:
        await db.rollback()
        raise e

    return LoginResponse(
        username=str(user.username), jwt=jwt, refresh_token=new_refresh_token
    )
