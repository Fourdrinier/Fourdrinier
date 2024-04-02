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

from passlib.context import CryptContext

from app.db.models import User
from app.db.schema import UserCreate
from app.db.session import get_db


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", status_code=201)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user
    """
    # Check if the user already exists
    existing_user = await db.get(User, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Ensure that if the user is to be a superuser, they have a valid registration token
    if user.is_superuser:
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
        is_superuser=user.is_superuser,
    )
    db.add(user_object)
    await db.commit()
    await db.refresh(user_object)

    # Return the user's username and superuser status
    return {"username": user_object.username, "is_superuser": user_object.is_superuser}
