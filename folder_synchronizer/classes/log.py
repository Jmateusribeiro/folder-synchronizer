"""
A custom logger class that logs messages to both console and file with timed rotation.
"""
import logging
import re
from logging import handlers, Logger
import os

class CustomLogger(Logger):

    def __init__(self, log_folder: str, backupCount_days: int = 30) -> None:
        """
        Initializes the custom logger.

        Args:
            log_folder (str): The directory where log files will be stored.
            backupCount_days (int): The number of days to keep backup log files.
        """
        super().__init__('CustomLogger')
        self.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

        # File handler (with timed rotation each day)
        file_handler = handlers.TimedRotatingFileHandler(
            os.path.join(log_folder, 'Folder_Sync'),
            when='midnight',
            backupCount=backupCount_days
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.suffix = '%Y_%m_%d.log'
        file_handler.extMatch = re.compile(r"^\d{4}_\d{2}_\d{2}.log$")
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)
