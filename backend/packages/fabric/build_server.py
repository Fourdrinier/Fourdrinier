"""
fabric/build_server.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 3 JAN 23

Build a server image given its settings
"""
import json
import os


def build_server(server):
    server = {"name": server.name, "game_version": server.game_version, "playset": None}

    # Determine required version of the OpenJDK
    with open(
        os.path.join(os.path.dirname(__file__), "java_compatibility.json"), "r"
    ) as file:
        java_compatability = json.load(file)
    java_requirement = java_compatability[server["game_version"]]

    # Set up the basics of the Dockerfile
    dockerfile_content = [
        f"FROM openjdk:{java_requirement}",
        "WORKDIR /minecraft",
    ]

    return dockerfile_content
