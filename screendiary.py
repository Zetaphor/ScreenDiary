import threading
import os
import asyncio
from dotenv import load_dotenv
from processing.capture import process_display
from logger_config import get_logger
from database import check_and_initialize_db, add_record
from util import empty_folder
from os_specific.kde.run_kwin_script import run_window_script
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method

load_dotenv()
logger = get_logger()

USE_DBUS_SERVER = os.getenv('WINDOW_TITLE_METHOD') == 'kde'

class DbusInterface(ServiceInterface):
    def __init__(self):
        super().__init__('com.screendiary.bridge')

    @method()
    def updateActiveWindow(self, resource_name: "s", resource_class: "s", caption: "s"):
        logger.debug(f'Active window: {resource_name}, {resource_class}, {caption}')

async def run_dbus_server():
    bus = await MessageBus().connect()
    interface = DbusInterface()
    bus.export('/com/screendiary/bridge', interface)
    await bus.request_name('com.screendiary.bridge')
    await bus.wait_for_disconnect()

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

def save_display_result(result):
    if result is None:
        logger.error('Received empty display result')
    add_record(result['datetime'], result['file_path'], result['ocr_title'], result['ocr_content'], result['url'], result['url_time'], result['url_partial'], result['should_ocr_content'], result['ocr_time'], result['application_name'])

def main():
    debug_reset()
    check_and_initialize_db()
    logger.debug('Window title method: ' + os.getenv('WINDOW_TITLE_METHOD'))

    if os.getenv('WINDOW_TITLE_METHOD') == 'kde':
        # Need to start the timer before dbus
        capture_timer(run_window_script, lambda val: None)
        logger.debug('Starting DBus server...')
        asyncio.run(run_dbus_server())

    elif os.getenv('WINDOW_TITLE_METHOD') == 'ocr':
        capture_timer(process_display, save_display_result)

if __name__ == '__main__':
    main()
