"""
get_user_from_jwt.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Decode a JWT and return the user object from the database.

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import DecodeError, InvalidAlgorithmError, ExpiredSignatureError
from jose import JWTError
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.db.models import User
from backend.app.dependencies.core.jwt.get_secret_key import get_secret_key

# Create an OAuth2 password bearer object
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user_from_jwt(token: str, db: AsyncSession) -> User:
    """
    Get the user from the JWT token
    """
    try:
        # Decode and extract the payload from the JWT
        payload: Any = jwt.decode(  # type: ignore
            token, get_secret_key(), algorithms=["HS256"]
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid bearer token")
    except DecodeError:
        raise HTTPException(status_code=401, detail="Invalid bearer token")
    except InvalidAlgorithmError:
        raise HTTPException(status_code=401, detail="Invalid bearer token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Invalid bearer token")

    # Extract the username from the payload
    username: str | None = payload.get("sub")
    if username is None or username == "":
        raise HTTPException(status_code=401, detail="Invalid bearer token")

    # Get the user from the database
    user: User | None = await db.get(
        User, username, options=[selectinload(User.servers)]
    )
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid bearer token")

    return user
