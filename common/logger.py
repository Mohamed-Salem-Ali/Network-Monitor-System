import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file):
    handler = RotatingFileHandler(log_file, maxBytes=5000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
