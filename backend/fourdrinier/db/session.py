"""
session.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Set up the database session for use by the FastAPI application.

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
