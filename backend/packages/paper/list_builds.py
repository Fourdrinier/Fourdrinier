"""
list_builds.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 28 DEC 23

List the available releases of Paper for a specified version of Minecraft
"""
import requests


def list_builds(version):
    url = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds"
    response = requests.get(url)
    if response.status_code == 404:
        raise Exception(f"No builds for version {version} were found.")
    response_json = response.json()
    builds = response_json["builds"]

    # Get the download URL
    for build in builds:
        build_id = build["build"]
        downloads = build["downloads"]
        application = downloads["application"]
        file = application["name"]
        build[
            "download_url"
        ] = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build_id}/downloads/{file}"

    return builds
