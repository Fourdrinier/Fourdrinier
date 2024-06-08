"""
registration_token.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Generate a registration token for new users

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os
import secrets


def generate_registration_token():
    # Generate the registration token
    registration_token = secrets.token_hex(16)

    # Write it to a file
    registration_token_file = os.environ.get(
        "REGISTRATION_TOKEN_FILE", "/var/lib/fourdrinier/registration_token"
    )
    try:
        with open(registration_token_file, "w") as f:
            f.write(registration_token)
    except IsADirectoryError:
        raise IsADirectoryError(f"{registration_token_file} is a directory, not a file")
    
    # Return the token
    return registration_token
