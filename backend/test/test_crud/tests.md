### get_servers() [GET /servers]
- **[000] test_crud_get_servers_000_nominal_no_servers**
    - Conditions: No servers in database
    - Result: []
- **[001] test_crud_get_servers_001_nominal_one_server**
    - Conditions: One server in database
    - Result: [\<server\>]