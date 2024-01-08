import json
import os


async def get_java_requirement(loader, game_version):
    with open(
        os.path.join(os.path.dirname(__file__), "java_compatibility.json"), "r"
    ) as file:
        java_compatability = json.load(file)
    return java_compatability[loader][game_version]
