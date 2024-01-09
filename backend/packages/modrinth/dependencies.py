import httpx


async def get_dependencies(version_ids):
    required_dependencies = []
    optional_dependencies = []

    version_id_string = (
        "[" + ", ".join(f'"{version_id}"' for version_id in version_ids) + "]"
    )

    # Get the metadata for a specific project version
    async with httpx.AsyncClient() as client:
        request = f"https://api.modrinth.com/v2/versions?ids={version_id_string}"
        response = await client.get(request)
        if response.status_code != 200:
            raise VersionNotFoundException
    versions = response.json()

    # Sort dependency project ID's by required and optional
    for version in versions:
        for dependency in version["dependencies"]:
            match dependency["dependency_type"]:
                case "required":
                    if dependency["project_id"] not in set(required_dependencies):
                        required_dependencies.append(dependency["project_id"])
                case "optional":
                    if dependency["project_id"] not in set(optional_dependencies):
                        optional_dependencies.append(dependency["project_id"])

    return required_dependencies, optional_dependencies


class VersionNotFoundException(Exception):
    pass
