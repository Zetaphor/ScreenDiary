import threading
import os
from dotenv import load_dotenv
from screenshot import process_screenshot
from logger_config import get_logger

load_dotenv()

logger = get_logger()

DEBUG = bool(int(os.getenv('DEBUG')))

def screenshot_timer(func):
    threading.Timer(int(os.getenv('SCREENSHOT_INTERVAL')), screenshot_timer, [func]).start()
    func()

def main():
    screenshot_timer(process_screenshot)

if __name__ == '__main__':
    main()