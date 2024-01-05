import threading
import os
from dotenv import load_dotenv
from image_processing.capture import process_display
from logger_config import get_logger
from database import check_and_initialize_db, add_record

load_dotenv()
logger = get_logger()


def debug_reset():
    if bool(int(os.getenv('DEBUG_RESET'))):
        logger.warning('Debug reset enabled, deleting images, ocr, and database...')
        os.unlink(os.getenv('DB_PATH'))

        if os.path.exists('./captures/screenshots'):
            empty_folder('captures/screenshots')

        if os.path.exists('./captures/ocr'):
            empty_folder('captures/ocr')

def capture_timer(func, callback):
    threading.Timer(int(os.getenv('SCREENSHOT_INTERVAL')), capture_timer, [func, callback]).start()
    result = func()
    callback(result)

def process_display_result(result):
    if result is None:
        logger.error('Received empty display result')
    add_record(result['datetime'], result['file_path'], result['ocr_title'], result['ocr_content'], result['url'], result['url_time'], result['url_partial'], result['should_ocr_content'], result['ocr_time'], result['application_name'])

def main():
    debug_reset()
    check_and_initialize_db()
    capture_timer(process_display, process_display_result)

if __name__ == '__main__':
    main()
