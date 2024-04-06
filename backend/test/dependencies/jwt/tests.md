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
