# logger.py
import logging
from colorlog import ColoredFormatter

def setup_logger(name=None):
    """
    Set up the logger with colored output to the console.
    
    Parameters:
    name (str): Optional name for the logger. If None, uses the root logger.

    Returns:
    logging.Logger: Configured logger instance.
    """
    # Create or get a logger
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if the function is called more than once
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(logging.INFO)

    # Create a formatter with color
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s%(reset)s - %(log_color)s%(levelname)s%(reset)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    # Create a console handler and set the formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger
