"""
app.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Main application file for the Fourdrinier project

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the MIT License. See the LICENSE file for more details.
"""

from fastapi import FastAPI
from app.api.v1.servers import router as servers_router
from app.api.v1.users import router as users_router

app = FastAPI()

# Include the routers
app.include_router(servers_router, prefix="/api/v1/servers", tags=["servers"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
