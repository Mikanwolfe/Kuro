import logging
import os

def cute_logger(name):
    # Create the logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Set up the logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Set up a FileHandler to save logs to disk
    file_handler = logging.FileHandler(f"logs/cute_{name}.log")
    logger.addHandler(file_handler)

    # Set up a formatter for the log messages
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)

    # Check if a file handler is already added
    if not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers):
        # Set up a FileHandler to save logs to disk
        file_handler = logging.FileHandler(f"logs/{name}.log")
        logger.addHandler(file_handler)

        # Set up a formatter for the log messages
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(formatter)

    return logger
