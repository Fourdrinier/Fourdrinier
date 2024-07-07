"""
get_config.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Get the configuration from config.json

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import os
import json


def get_config():
    config_filepath = os.path.join(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        ),
        "config.json",
    )

    with open(config_filepath, "r") as config_file:
        config = json.load(config_file)

    return config
