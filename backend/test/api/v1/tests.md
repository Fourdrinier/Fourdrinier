# API v1

## /servers

### list_servers() [GET /servers]
- **[000] test_list_servers_000_nominal_no_servers**
    - Conditions: No servers in database
    - Result: HTTP 200 - No servers returned
- **[001] test_list_servers_001_nominal_one_server**
    - Conditions: One server in database
    - Result: HTTP 200 - Server object returned

### create_server() [POST /servers]
- **[000] test_create_server_000_nominal**
    - Conditions: One valid server object
    - Result: HTTP 201: Server object created and returned
- **[001] test_create_server_001_unauthorized**
    - Conditions: Invalid user
    - Result: HTTP 403 - Unauthorized


