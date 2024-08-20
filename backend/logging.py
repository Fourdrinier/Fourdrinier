"""
logging.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Logging configuration

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Fourdrinier project and is released under
the GPLv3 License. See the LICENSE file for more details.
"""

import logging
import os
from datetime import datetime


# Get the log filename
log_directory = "/fourdrinier/logs"
log_filename: str = os.path.join(
    log_directory, datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
)

# Get the logger
logger: logging.Logger = logging.getLogger("Fourdrinier")
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and attach it to the handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Use the logger
logger.debug("This message goes to console only")
logger.error("This message goes to both console and file")
