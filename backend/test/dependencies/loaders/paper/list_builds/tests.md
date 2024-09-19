# list_builds() (Paper)

## Test Plan
- Nominal
- Connection cannot be established
- Connection times out
- Undetermined issue within PaperMC API
- Version does not exist

## Test Specifications
- **[000] test_paper_list_builds_000_nominal**
    - Conditions: Version = 1.21
    - Result: HTTP 200

            [
                {
                    "build_id": 1,
                    "filename": "paper-1.21-1.jar",
                    "url": "https://api.papermc.io/v2/projects/paper/versions/1.21/builds/1/downloads/paper-1.21-1.jar"                    
                 }
            ]

- **[001] test_paper_list_builds_001_anomalous_connection_failed**
    - Conditions: Connection fails
    - Result: `RuntimeError("Failed to connect to the PaperMC API")`
- **[002] test_paper_list_builds_002_anomalous_connection_timeout**
    - Conditions: Connection forcibly times out
    - Result: `RuntimeError("Connection to the PaperMC API timed out")`
- **[003] test_paper_list_builds_003_anomalous_api_failure**
    - Conditions: PaperMC returns an HTTP 500
    - Result: `RuntimeError("PaperMC API failed for unknown reason. Status Code: 500")`
- **[004] test_paper_list_builds_004_anomalous_nonexistent_version**
    - Conditions: version = "1.21.0" (Paper uses 1.21)
    - Result: HTTP 404 - Version not found