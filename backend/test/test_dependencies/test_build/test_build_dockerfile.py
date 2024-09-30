"""
test_build_dockerfile.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test build_dockerfile()

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import textwrap

from backend.fourdrinier.dependencies.build.build_image import build_dockerfile


async def test_build_dockerfile_000_nominal() -> None:
    """
    Test 000 - Nominal
    Conditions: jdk_version=17, loader_url="https://example.com/server.jar", server_port=25565, min_memory=2048, max_memory=2048
    Result: Dockerfile content returned
    """
    # Call the function
    dockerfile: str = await build_dockerfile(
        17, "https://example.com/server.jar", 25565, 2048, 2048
    )

    # Check the result
    assert (
        dockerfile
        == textwrap.dedent(
            """
        FROM openjdk:17

        # Set the working directory of the image
        WORKDIR /server

        # Download the server jar
        ADD https://example.com/server.jar /server/server.jar

        # Expose the port for incoming connections
        EXPOSE 25565

        # Run the server
        CMD java -Xms2048M -Xmx2048M -jar server.jar
        """
        ).strip()
    )
