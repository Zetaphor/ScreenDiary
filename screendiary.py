import threading
import os
import asyncio
from dotenv import load_dotenv
from server.processing.capture import process_display
from server.logger_config import get_logger
from server.database import check_and_initialize_db, add_record
from server.util import empty_folder, load_ignore_lists, load_application_name_remaps, reset_logs
from server.os_specific.kde.run_kwin_script import run_window_script
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method
from server.idle_monitor import IdleMonitor
from server.processing.batch_process import process_next_batch
import server.webserver

load_dotenv()
logger = get_logger()

USE_DBUS_SERVER = os.getenv('WINDOW_TITLE_METHOD') == 'kde'
DEBUG_DBUS_WINDOW = bool(int(os.getenv('DEBUG_DBUS_WINDOW')))

batch_processing_active = False
batch_processing_timer = None

class DbusInterface(ServiceInterface):
    def __init__(self):
        super().__init__('com.screendiary.bridge')

    @method()
    def updateActiveWindow(self, resource_name: "s", resource_class: "s", caption: "s"):
        if DEBUG_DBUS_WINDOW:
            logger.debug(f'Active Window | Name: {resource_name}, Class: {resource_class}, Caption: {caption}')
        # result = process_display(False, {'name': resource_name, 'class': resource_class, 'caption': caption})
        # save_display_result(result)

async def run_dbus_server():
    bus = await MessageBus().connect()
    interface = DbusInterface()
    bus.export('/com/screendiary/bridge', interface)
    await bus.request_name('com.screendiary.bridge')
    await bus.wait_for_disconnect()

def debug_reset():
    if bool(int(os.getenv('DEBUG_RESET_LOGS'))):
        logger.warning('Debug reset logs enabled, deleting logs...')
        reset_logs()

    if bool(int(os.getenv('DEBUG_RESET'))):
        logger.warning('Debug reset enabled, deleting images, ocr, and database...')
        os.unlink(os.getenv('DB_PATH'))

        if os.path.exists('./captures/screenshots'):
            empty_folder('captures/screenshots')

        if os.path.exists('./captures/ocr'):
            empty_folder('captures/ocr')

def run_batch_processing():
    global batch_processing_timer, batch_processing_active
    if not batch_processing_active:
        return

    process_next_batch()

    # Reschedule the timer
    batch_processing_timer = threading.Timer(2, run_batch_processing)
    batch_processing_timer.start()

def stop_batch_processing():
    global batch_processing_timer
    if batch_processing_timer:
        batch_processing_timer.cancel()
        batch_processing_timer = None

def capture_timer(func, callback):
    threading.Timer(int(os.getenv('SCREENSHOT_INTERVAL')), capture_timer, [func, callback]).start()
    result = func()
    callback(result)

def save_display_result(result):
    if result is None:
        return
    add_record(result)

def main():
    global batch_processing_active, batch_processing_timer
    # debug_reset()
    # check_and_initialize_db()
    load_ignore_lists()
    load_application_name_remaps()
    logger.debug('Window title method: ' + os.getenv('WINDOW_TITLE_METHOD'))

    # Start capturing screenshots
    if os.getenv('WINDOW_TITLE_METHOD') == 'kde':
        capture_timer(run_window_script, lambda val: None)
        logger.debug('Starting DBus server...')
        loop = asyncio.new_event_loop()
        dbus_thread = threading.Thread(target=lambda: loop.run_until_complete(run_dbus_server()), daemon=True)
        dbus_thread.start()
    elif os.getenv('WINDOW_TITLE_METHOD') == 'ocr':
        logger.debug('Starting OCR loop...')
        capture_timer(process_display, save_display_result)

    logger.debug('Starting idle monitor...')
    monitor = IdleMonitor()
    monitor_thread = threading.Thread(target=monitor.monitor_input, daemon=True)
    monitor.reset_timer()
    monitor_thread.start()
    server.webserver.start_web_server()

    while True:
        if monitor.has_inactivity():
            if not batch_processing_active:
                logger.debug('Inactivity detected, starting batch processing...')
                batch_processing_active = True
                run_batch_processing()
        else:
            if batch_processing_active:
                logger.debug('Activity detected, stopping batch processing...')
                batch_processing_active = False
                stop_batch_processing()

if __name__ == '__main__':
    main()
