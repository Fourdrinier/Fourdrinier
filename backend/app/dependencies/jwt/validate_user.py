"""
validate_user.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Validate a user from a JWT token

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.jwt.get_user_from_jwt import get_user_from_jwt

from app.db.models import User
from app.db.session import get_db

# Create an OAuth2 password bearer object
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def validate_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """Validate a user from a JWT token"""
    user = await get_user_from_jwt(token, db)
    return user
