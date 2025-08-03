import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Set up log file handler rotating daily
log_file = "logs/app.log"
handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=30, encoding="utf-8")
handler.suffix = "%Y-%m-%d"

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d (%(funcName)s) - %(message)s"
)
handler.setFormatter(formatter)

logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
