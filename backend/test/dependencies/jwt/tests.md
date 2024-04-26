# JWT

### get_secret_key()
- **[000] test_get_secret_key_000_nominal_secret_key**
    - Conditions: Environment variable "JWT_SECRET_KEY" is set as a string
    - Result: Secret key string returned
- **[001] test_get_secret_key_001_anomalous_secret_key_var_not_set**
    - Conditions: Environment variable "JWT_SECRET_KEY" is not set
    - Result: EnvironmentError("The environment variable JWT_SECRET_KEY cannot be empty")
- **[002] test_get_secret_key_002_anomalous_secret_key_var_empty**
    - Conditions: Environment variable "JWT_SECRET_KEY" is an empty string
    - Result: EnvironmentError("The environment variable JWT_SECRET_KEY cannot be empty")
- **[003] test_get_secret_key_003_anomalous_secret_key_too_short**
    - Conditions: Environment variable "SECRET_KEY" is a string that is < 256 bits (64 characters) long
    - Result: ValueError("Secret key must be at least 256 bits (64 hexadecimal characters) long")


### get_jwt_expieration_time()
- **[000] test_get_jwt_expiration_time_000_nominal_expiration_time**
    - Conditions: Environment variable "JWT_EXPIRATION_TIME" is set to 1 (minutes)
    - Result: Integer `1` returned
- **[001] test_get_jwt_expiration_time_001_anomalous_var_not_set**
    - Conditions: Environment variable "JWT_EXPIERATION_TIME" is not set
    - Result: EnvironmentError("The environment variable JWT_EXPIRATION_TIME cannot be empty")
- **[002] test_get_jwt_expiration_time_002_anomalous_var_empty**
    - Conditions: Environment variable "JWT_EXPIRATION_TIME" is an empty string
    - Result: EnvironmentError("The environment variable JWT_EXPIRATION_TIME cannot be empty")
- **[003] test_get_jwt_expiration_time_003_anomalous_not_digit**
    - Conditions: Environment variable "JWT_EXPIRATION_TIME" = "not_an_integer"
    - Result: ValueError("The environment variable JWT_EXPIRATION_TIME must be an integer"
    )
- **[003] test_get_jwt_expiration_time_004_anomalous_non_integer**
    - Conditions: Environment variable "JWT_EXPIRATION_TIME" = 1.5
    - Result: ValueError("The environment variable JWT_EXPIRATION_TIME must be an integer"
    )
- **[004] test_get_jwt_expiration_time_005_anomalous_less_than_one**
    - Conditions: Environment variable "JWT_EXPIRATION_TIME" = 0
    - Result: ValueError("The environment variable JWT_EXPIRATION_TIME must be >= 1 (in minutes)")


### generate_jwt()
- **[000] test_generate_jwt_000_nominal**
    - Conditions: Username provided
    - Result: JWT returned
- **[001] test_generate_jwt_001_anomalous_no_username**
    - Conditions: username = None
    - Result: ValueError('username' must be of type <class 'str'>, not <class 'NoneType'>)
- **[002] test_generate_jwt_002_anomalous_username_is_not_string**
    - Conditions: username = 1
    - Result: ValueError('username' must be of type <class 'str'>, not <class 'int'>)


### get_user_from_jwt()
- **[000] test_get_user_from_jwt_000_nominal**
    - Conditions: Valid JWT
    - Result: User object returned
- **[001] test_get_user_from_jwt_001_anomalous_bad_token_missing_header**
    - Conditions: JWT is missing header
    - Result: HTTP 401 - Invalid bearer token
- **[002] test_get_user_from_jwt_002_anomalous_bad_token_missing_payload**
    - Conditions: JWT is missing its payload
    - Result: HTTP 401 - Invalid bearer token
- **[003] test_get_user_from_jwt_003_anomalous_bad_token_missing_signature**
    - Conditions: JWT is missing a signature
    - Result: HTTP 401 - Invalid bearer token
- **[004] test_get_user_from_jwt_004_anomalous_bad_token_extra_data**
    - Conditions: Token contains extra data beyond header, payload, and signature
    - Result: HTTP 401 - Invalid bearer token
- **[005] test_get_user_from_jwt_005_anomalous_bad_token_no_alg**
    - Conditions: No algorithm specified in header
    - Result: HTTP 401 - Invalid bearer token
- **[006] test_get_user_from_jwt_006_anomalous_bad_token_invalid_json**
    - Conditions: The contents of the payload is not valid JSON
    - Result: HTTP 401 - Invalid bearer token
- **[007] test_get_user_from_jwt_007_anomalous_invalid_token_expired**
    - Conditions: The token is expired
    - Result: HTTP 401 - Invalid bearer token
- **[008] test_get_user_from_jwt_008_anomalous_invalid_token_missing_username**
    - Conditions: The token payload is missing a username
    - Result: HTTP 401 - Invalid bearer token
- **[009] test_get_user_from_jwt_009_anomalous_invalid_token_invalid_username**
    - Conditions: The specified username does not exist
    - Result: HTTP 401 - Invalid bearer token
- **[010] test_get_user_from_jwt_009_anomalous_invalid_signature**
    - Conditions: The signature does not match the server's signature
    - Result: HTTP 401 - Invalid bearer token