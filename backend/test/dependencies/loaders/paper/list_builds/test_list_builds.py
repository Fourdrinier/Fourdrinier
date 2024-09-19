"""
test_list_builds.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Test the list_builds function in the paper loader

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import requests
from unittest.mock import AsyncMock, MagicMock, NonCallableMagicMock
import pytest
from pytest_mock.plugin import MockerFixture
from typing import Dict

from backend.app.dependencies.loaders.paper.list_builds import list_builds


@pytest.mark.asyncio
async def test_paper_list_builds_000_nominal(mocker: MockerFixture) -> None:
    """
    Test 000 - Nominal
    Conditions: PaperMC API returns a successful response
    Result: Builds are returned
        [
            {
                "build_id": 1,
                "filename": "paper-1.21-1.jar",
                "url": "https://api.papermc.io/v2/projects/paper/versions/1.21/builds/1/downloads/paper-1.21-1.jar"
            }
        ]
    """
    # Mock the output of the PaperMC API
    mock_get: MagicMock | AsyncMock | NonCallableMagicMock = mocker.patch(
        "requests.get"
    )
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "project_id": "paper",
        "project_name": "Paper",
        "version": "1.21",
        "builds": [
            {
                "build": 1,
                "time": "2024-06-17T19:46:12.027Z",
                "channel": "experimental",
                "promoted": False,
                "changes": [
                    {
                        "commit": "21c9a7c79de2e49abfbb6a9bd69621d3b75f230b",
                        "summary": "Rebuild patches",
                        "message": "Rebuild patches\n",
                    }
                ],
                "downloads": {
                    "application": {
                        "name": "paper-1.21-1.jar",
                        "sha256": "b7d25fff70fa5583fb1f65249296dcc03cf214189d93dc275d6349ada184b843",
                    }
                },
            },
        ],
    }

    builds: list[Dict[str, str]] = await list_builds("1.21")
    assert builds == [
        {
            "build_id": 1,
            "filename": "paper-1.21-1.jar",
            "url": "https://api.papermc.io/v2/projects/paper/versions/1.21/builds/1/downloads/paper-1.21-1.jar",
        }
    ]


@pytest.mark.asyncio
async def test_paper_list_builds_001_anomalous_connection_failed(
    mocker: MockerFixture,
) -> None:
    """
    Test 001 - Anomalous
    Conditions: Connection to the PaperMC API fails
    Result: `RuntimeError("Failed to connect to the PaperMC API")`
    """
    # Mock the output of the PaperMC API
    mock_get: MagicMock | AsyncMock | NonCallableMagicMock = mocker.patch(
        "requests.get"
    )
    mock_get.side_effect = requests.exceptions.ConnectionError

    with pytest.raises(RuntimeError) as e:
        await list_builds("1.21")
    assert str(e.value) == "Failed to connect to the PaperMC API"


@pytest.mark.asyncio
async def test_paper_list_builds_002_anomalous_connection_timeout(
    mocker: MockerFixture,
) -> None:
    """
    Test 002 - Anomalous
    Conditions: Connection forcibly times out
    Result: `RuntimeError("Connection to the PaperMC API timed out")`
    """
    # Mock the output of the PaperMC API
    mock_get: MagicMock | AsyncMock | NonCallableMagicMock = mocker.patch(
        "requests.get"
    )
    mock_get.side_effect = requests.exceptions.Timeout

    with pytest.raises(RuntimeError) as e:
        await list_builds("1.21")
    assert str(e.value) == "Connection to the PaperMC API timed out"


@pytest.mark.asyncio
async def test_paper_list_builds_003_anomalous_api_failure(
    mocker: MockerFixture,
) -> None:
    """
    Test 003 - Anomalous
    Conditions: PaperMC returns an HTTP 500
    Result: `RuntimeError("PaperMC API failed for unknown reason. Status Code: 500")`
    """
    # Mock the output of the PaperMC API
    mock_get: MagicMock | AsyncMock | NonCallableMagicMock = mocker.patch(
        "requests.get"
    )
    mock_get.return_value.status_code = 500

    with pytest.raises(RuntimeError) as e:
        await list_builds("1.21")
    assert str(e.value) == "PaperMC API failed for unknown reason. Status Code: 500"
