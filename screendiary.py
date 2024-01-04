import threading
import os
from dotenv import load_dotenv
from capture import process_display
from logger_config import get_logger
from database import check_and_initialize_db, add_record, reset_tables
from util import parse_application_name

load_dotenv()

logger = get_logger()

DEBUG = bool(int(os.getenv('DEBUG')))

def capture_timer(func, callback):
    threading.Timer(int(os.getenv('SCREENSHOT_INTERVAL')), capture_timer, [func, callback]).start()
    result = func()
    callback(result)

def process_display_result(result):
    if result is None:
        return
    add_record(result['datetime'], result['file_path'], result['ocr_title'], result['ocr_content'], result['url'], result['should_ocr_content'], result['application_name'])

def main():
    check_and_initialize_db()
    reset_tables()
    capture_timer(process_display, process_display_result)

if __name__ == '__main__':
    main()
