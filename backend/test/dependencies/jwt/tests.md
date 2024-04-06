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
    - Conditions: Environment variable "JWT_EXPIRATION_TIME" is set to 60 (minutes)
    - Result: Integer `60` returned
- **[001] test_get_jwt_expiration_time_001_anomalous**
    - Conditions:
    - Result:
- **[002] test_get_jwt_expiration_time_002_anomalous**
    - Conditions:
    - Result:
- **[003] test_get_jwt_expiration_time_003_anomalous**
    - Conditions:
    - Result:
- **[004] test_get_jwt_expiration_time_004_anomalous**
    - Conditions:
    - Result:
- **[005] test_get_jwt_expiration_time_005_anomalous**
    - Conditions:
    - Result:

### generate_jwt()
- **[000] test_generate_jwt_000_anomalous_no_username**
    - Conditions: No username provided
    - Result: ValueError('username' must be of type <class 'str'>, not <class 'NoneType'>)
- **[001] test_generate_jwt_001_anomalous_username_is_not_string**
    - Conditions: Username is a string
    - Result: ValueError('username' must be of type <class 'str'>, not <class 'int'>)
