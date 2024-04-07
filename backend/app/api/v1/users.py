"""
users.py

@Author: Ethan Brown - ethan@ewbrowntech.com

All endpoints for users

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import secrets
from passlib.context import CryptContext

from app.db.models import User
from app.db.schema import UserCreate, UserLogin
from app.db.session import get_db

from app.dependencies.jwt.generate_jwt import generate_jwt

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/superuser", status_code=201)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new superuser
    """
    # Check if there are already users in the database. If so, make the endpoint unavailable
    result = await db.execute(select(User))
    users = result.scalars().all()
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
    hashed_password = pwd_context.hash(user.password)

    # Create the user
    user_object = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_superuser=True,
    )
    db.add(user_object)
    await db.commit()
    await db.refresh(user_object)

    # Return the user's username and superuser status
    return {"username": user_object.username, "is_superuser": user_object.is_superuser}


@router.post("/login", status_code=200)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Log in a user
    """
    # Get the user from the database
    result = await db.execute(select(User).where(User.username == user.username))
    user_object = result.scalars().first()

    # Check if the user exists
    if not user_object:
        raise HTTPException(status_code=404, detail="The provided credentials were incorrect")

    # Check the password
    if not pwd_context.verify(user.password, user_object.hashed_password):
        raise HTTPException(status_code=401, detail="The provided credentials were incorrect")

    # Create a JWT
    jwt = generate_jwt(username=user.username)

    # Create a refresh token
    refresh_token = secrets.token_hex(32)
    user_object.refresh_token = refresh_token
    await db.commit()
    await db.refresh(user_object)

    # Return the user's username and superuser status
    return {"username": user_object.username, "jwt": jwt, "refresh_token": user_object.refresh_token}