import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_custom_logger(name):
    # cwd = str(os.getcwd())
    script_dir = os.path.dirname(__file__)
    formatter_file = logging.Formatter(
        "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    )
    try:
        os.makedirs(os.path.join(script_dir, "logs"))
    except FileExistsError:
        pass
    path = os.path.join(script_dir, "logs", "trace.log")
    handler = TimedRotatingFileHandler(path, when="d", interval=1, backupCount=10)
    handler.setFormatter(formatter_file)
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.INFO)
    logger.addHandler(handler)
    return logger
