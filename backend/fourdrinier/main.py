"""
main.py

@Author: Ethan Brown - ethan@ewbrowntech.com

This is the main file for the FastAPI application. It contains the FastAPI
application object and all of the routes for the application.

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os
from typing import Dict

from fastapi import FastAPI

from backend.fourdrinier.api.servers import router as servers_router
from backend.fourdrinier.core.config import PROJECT_NAME


# Initialize the FastAPI application object
app = FastAPI(title=PROJECT_NAME)

# Set up SSH connections to Docker hosts
docker_host: str | None = os.getenv("DOCKER_HOST")
if docker_host:
    os.system(f"ssh-keyscan -H {docker_host.split('@')[1]} >> ~/.ssh/known_hosts")

# Include the routers
app.include_router(servers_router, prefix="/servers")


# Create a health check route
@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "ok"}
