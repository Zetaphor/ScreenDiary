import threading
import os
from dotenv import load_dotenv
from capture import process_display
from logger_config import get_logger
from database import check_and_initialize_db, add_record, reset_tables

load_dotenv()

logger = get_logger()

DEBUG = bool(int(os.getenv('DEBUG')))

def capture_timer(func, callback):
    threading.Timer(int(os.getenv('SCREENSHOT_INTERVAL')), capture_timer, [func, callback]).start()
    result = func()
    callback(result)

def parse_application_name(title):
    # Finding the index of the last occurrence of a dash (hyphen, en dash, em dash)
    last_hyphen = title.rfind(' - ')
    last_en_dash = title.rfind(' – ')
    last_em_dash = title.rfind(' — ')

    # Get the position of the last dash, whichever it is
    last_dash = max(last_hyphen, last_en_dash, last_em_dash)

    # If a dash is found, slice the string from that point
    if last_dash != -1:
        return title[last_dash + 3:]  # +3 to skip the dash and the spaces
    else:
        return "Unknown"

def process_display_result(result):
    if result is None:
        return
    application_name = parse_application_name(result['ocr_title'])
    add_record(result['datetime'], result['file_path'], result['ocr_title'], result['ocr_content'], application_name)


def main():
    check_and_initialize_db()
    reset_tables()
    capture_timer(process_display, process_display_result)


if __name__ == '__main__':
    main()
