import os
import logging
from datetime import datetime

class Logger:
    def __init__(self, log_dir="logs/", print_to_console=True):
        # Store user preferences
        self.log_dir = log_dir
        self.print_to_console = print_to_console

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = os.path.join(self.log_dir, f"log_{today}.txt")

         # Set up the core logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers = []

        # File handler writes logs to file
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s — %(levelname)s — %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

        # While True, add console output
        if self.print_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

"""future additions
    getting rid of out-dated logs (keep last 7 days or so)
    separate log files from different modules (scraper, report_generator, etc.)
"""