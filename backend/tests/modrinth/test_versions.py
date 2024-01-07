import pytest

from backend.packages.modrinth.versions import get_versions


@pytest.mark.asyncio
async def test_get_version():
    project_id = "o1C1Dkj5"
    game_versions = ["1.20.1"]
    versions = await get_versions(project_id, game_versions)
    version_ids = []
    for version in versions:
        version_ids.append(version["id"])
    assert "sZO4lGuf" in version_ids
