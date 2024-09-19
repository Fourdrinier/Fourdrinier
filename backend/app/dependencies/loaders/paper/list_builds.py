"""
list_builds.py

@Author: Ethan Brown - ethan@ewbrowntech.com

List all builds for a paper

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import requests
from typing import Any


async def list_builds(version: str) -> list[dict[str, str]]:
    url: str = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds"

    # Make a request to the PaperMC API
    try:
        response: requests.Response = requests.get(url)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Failed to connect to the PaperMC API")
    except requests.exceptions.Timeout:
        raise RuntimeError("Connection to the PaperMC API timed out")

    if response.status_code == 200:
        data: Any = response.json()
    elif response.status_code == 404:
        raise RuntimeError("Version not found")
    else:
        raise RuntimeError(
            f"PaperMC API failed for unknown reason. Status Code: {response.status_code}"
        )

    # Extract the build data
    if "builds" not in data:
        raise RuntimeError("No build data found")
    builds: list[dict[str, str]] = []

    # Interpret the build URLs
    for build in data["builds"]:
        build_id: str = build["build"]
        file: str = build["downloads"]["application"]["name"]  # type: ignore
        builds.append(
            {
                "build_id": build_id,
                "filename": file,
                "url": f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build_id}/downloads/{file}",
            }
        )

    return builds
