# /servers/

## create_server() [POST /servers/]
- **[000] test_create_server_000_nominal**
    - Conditions: One valid server object
    - Result: HTTP 201 - Server object returned

## list_servers() [GET /servers/]
- **[000] test_list_servers_000_nominal_no_servers**
    - Conditions: No servers in database
    - Result: HTTP 200 - []
- **[001] test_list_servers_001_nominal_two_servers**
    - Conditinos: Two servers in database
    - Result: HTTP 200 - [`server1`, `server2`]

## get_server() [GET /servers/{server_id}]
- **[000] test_get_server_000_nominal**
    - Conditions: Server1 in database, request Server1
    - Result: HTTP 200 - `server1`
- **[001] test_get_server_001_anomalous_nonexistent_server**
    - Conditions: Server1 in database, request Server2
    - Result: HTTP 404 - "Server not found"