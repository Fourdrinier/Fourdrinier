import httpx


async def get_dependencies(version_ids, ignored_dependencies):
    required_dependencies = []
    optional_dependencies = []

    # Get the metadata for a specific project version
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.modrinth.com/v2/version?ids={version_ids}"
        )
        if response.status_code != 200:
            raise VersionNotFoundException
    dependencies = response.json()["dependencies"]

    # Sort dependency project ID's by required and optional
    for dependency in dependencies:
        if dependency["project_id"] in ignored_dependencies:
            continue
        match dependency["dependency_type"]:
            case "required":
                required_dependencies.append(dependency["project_id"])
            case "optional":
                optional_dependencies.append(dependency["project_id"])

    return required_dependencies, optional_dependencies


class VersionNotFoundException(Exception):
    pass
