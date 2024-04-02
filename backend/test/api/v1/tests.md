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

### register_user() [POST /users]
- **[000] test_register_user_000_nominal_superuser**
    - Conditions: No users in database
    - Result: HTTP 201: Superuser created
- **[001] test_register_user_001_nominal_standard_user**
    - Conditions: One superuser in database
    - Result: HTTP 201: Standard user created
- **[002] test_register_user_002_anomalous_superuser_no_token**
    - Conditions: Invalid token included in request to create superuser
    - Result: HTTP 400: Please include registration token found in $REGISTRATION_TOKEN_PATH
- **[004] test_register_user_003_anomalous_username_taken**
    - Conditions: User with username in database
    - Result: HTTP 400: That username is unavailable
