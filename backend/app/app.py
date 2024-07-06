"""
app.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Main application file for the Fourdrinier project

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

from fastapi import FastAPI
from backend.app.api.v1.servers import router as servers_router
from backend.app.api.v1.users import router as users_router
from backend.app.api.v1.playsets import router as playsets_router

from backend.app.dependencies.registration_token.registration_token import (
    generate_registration_token,
)
import os

print(os.environ.get("CONTAINER_ENV"))

# Check if running in a container
if os.environ.get("CONTAINER_ENV") == "true":
    # Generate the registration token
    REGISTRATION_TOKEN = generate_registration_token()

# Create the FastAPI app
app = FastAPI()

# Include the routers
app.include_router(servers_router, prefix="/api/v1/servers", tags=["servers"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(playsets_router, prefix="/api/v1/playsets", tags=["playsets"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
