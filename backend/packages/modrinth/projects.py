import httpx


async def get_projects(project_ids):
    # This string casting must be done this way such that the elements
    # will appear with double quotes around them in the API request
    projects_string = (
        "[" + ", ".join(f'"{project_id}"' for project_id in project_ids) + "]"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.modrinth.com/v2/projects?ids={projects_string}"
        )
    projects = response.json()
    located_project_ids = [project["id"] for project in projects]
    missing_project_ids = [
        project_id
        for project_id in project_ids
        if project_id not in located_project_ids
    ]
    if len(missing_project_ids) > 0:
        raise ProjectNotFoundException(missing_project_ids)

    return projects


class ProjectNotFoundException(Exception):
    def __init__(self, missing_project_ids):
        message = f"Projects with ids {missing_project_ids} not found on Modrinth API"
        super().__init__(message)
