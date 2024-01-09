from loguru import logger
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = bool(int(os.getenv('DEBUG')))
log_level = 'DEBUG' if DEBUG else 'INFO'

# Generate a timestamp for the log file name
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_path = f"logs/log_{timestamp}.log"

# Configure the logger
logger.add(log_file_path, rotation="1 week", level=log_level)

def get_logger():
    return logger
