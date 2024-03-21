# API v1

## /servers

### list_servers() [GET /servers]
- **[000] test_list_servers_000_nominal_no_servers**
    - Conditions: No servers in database
    - Result: No servers returned
- **[001] test_list_servers_001_nominal_one_server**
    - Conditions: One server in database
    - Result: Server object returned