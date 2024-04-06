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


## /users

### register_superuser() [POST /users/superuser]
- **[000] test_register_superuser_000_nominal_superuser**
    - Conditions: No users in database
    - Result: HTTP 201: Superuser created
- **[001] test_register_superuser_001_anomalous_superuser_present**
    - Conditions: One superuser in database
    - Result: HTTP 404
- **[002] test_register_superuser_002_anomalous_no_token**
    - Conditions: No token included in request for superuser
    - Result: HTTP 400: Superuser registration requires a registration token
- **[003] test_register_superuser_003_anomalous_invalid_token**
    - Conditions: Invalid token included in request to register superuser
    - Result: HTTP 400: Invalid registration token