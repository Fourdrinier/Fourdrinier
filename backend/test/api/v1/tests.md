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
- **[001] test_create_server_001_anomalous_unauthorized**
  - Conditions: Invalid user
  - Result: HTTP 403 - Unauthorized
- **[002] test_create_server_002_anomalous_invalid_loader**
  - Conditions: loader = "invalid"
  - Result: HTTP 400 - Validation error
- **[003] test_create_server_003_anomalous_invalid_game_version**
  - Conditions: game_version = "invalid"
  - Result: HTTP 422 - "String should match pattern '^\\d+\\.\\d+\\.\\d+$'"
- **[004] test_create_server_004_anomalous_unsupported_game_version**
  - Conditions: game_version = 2.0.0
  - Result: HTTP 400 - "Unsupported game version"
- **[005] test_create_server_005_anomalous**
  - Conditions:
  - Result:
- **[006] test_create_server_006_anomalous**
  - Conditions:
  - Result:
- **[007] test_create_server_007_anomalous**
  - Conditions:
  - Result:


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


### login() [POST /users/login]
- **[000] test_login_000_nominal**
  - Conditions: Correct username and password provided
  - Result: HTTP 200 - JWT and refresh token returned
- **[001] test_login_001_anomalous_no_username_provided**
  - Conditions: Password provided, but username missing
  - Result: HTTP 400 - {Pydantic error}
- **[002] test_login_002_anomalous_no_password_provided**
  - Conditions: Username provided, but password missing
  - Result: HTTP 400 - {Pydantic error}
- **[003] test_login_003_anomalous_nonexistent_username**
  - Conditions: Username provided does not exist
  - Result: HTTP 401 - "The provided credentials were incorrect"
- **[004] test_login_004_anomalous_incorrect_password**
  - Conditions: Incorrect password provided
  - Result: HTTP 401 - "The provided credentials were incorrect"


### refresh() [POST /users/refresh]
- **[000] test_refresh_000_nominal**
  - Conditions: Valid username and refresh token given
  - Result: HTTP 201 - New JWT and refresh token returned
- **[001] test_refresh_001_anomalous_no_token**
  - Conditions: Valid username given, no refresh token given
  - Result: HTTP 422 - Pydantic error
- **[002] test_refresh_002_anomalous_no_username**
  - Conditions: No username given, valid refresh token given
  - Result: HTTP 422 - Pydantic error
- **[003] test_refresh_003_anomalous_invalid_username**
  - Conditions: Invalid username given
  - Result: HTTP 401 - "The provided credentials were incorrect"
- **[004] test_refresh_004_anomalous_invalid_token**
  - Conditions: Invalid refresh token given
  - Result: HTTP 401 - "The provided credentials were incorrect"
- **[005] test_refresh_005_anomalous_invalid_username_and_token**
  - Conditions: Invalid username and refresh token given
  - Result: HTTP 401 - "The provided credentials were incorrect"


## /playsets

### list_playsets() [GET /playsets]
- **[000] test_list_playsets_000_nominal_no_playsets**
  - Conditions: User is superuser, no playsets in db
  - Result: HTTP 200 - []
- **[000] test_list_playsets_001_nominal_no_playsets_available**
  - Conditions: User test-user1 is not a superuser, user test-user2 has one private playset
  - Result: HTTP 200 - []