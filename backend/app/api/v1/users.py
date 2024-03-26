"""
users.py

@Author: Ethan Brown - ethan@ewbrowntech.com

All endpoints for users

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the MIT License. See the LICENSE file for more details.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.db.models import User

router = APIRouter()


@router.post("/register", status_code=201)
async def register_user():
    """
    Register a new user
    """
    return {"message": "User registered"}
