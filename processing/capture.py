import os
import time
from datetime import datetime
from PIL import Image
import imagehash
from dotenv import load_dotenv
from logger_config import get_logger
from util import get_ocr_ignore_list
from processing.ocr import ocr_titlebar, ocr_content
from processing.browser import capture_url
from processing.screenshot import take_screenshot

load_dotenv()

logger = get_logger()

DEBUG = bool(int(os.getenv('DEBUG')))
DEBUG_OCR = bool(int(os.getenv('DEBUG_OCR')))

LIVE_OCR_CONTENT = bool(int(os.getenv('LIVE_OCR_CONTENT')))
OCR_UNKNOWN_APPLICATIONS = bool(int(os.getenv('OCR_UNKNOWN_APPLICATIONS')))

CAPTURE_BROWSER_URL = bool(int(os.getenv('CAPTURE_BROWSER_URL')))
BROWSER_HISTORY_MATCH_TIME_RANGE = int(os.getenv('BROWSER_HISTORY_MATCH_TIME_RANGE'))

ocr_ignore_list = get_ocr_ignore_list('./ignore_ocr.conf')

phash = None
dhash = None
previous_dhash = None
previous_phash = None

def process_display(use_title_ocr=True, window_data=None):
    """
    Take a screenshot and process it to extract the titlebar and content
    If use_title_ocr is True, then OCR the titlebar and content, otherwise
    use window_data to set the window titlebar
    """
    global phash, dhash, previous_dhash, previous_phash
    start_time = time.time()

    os.makedirs(f"./captures/screenshots", exist_ok=True)

    datetime_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_file = f"./captures/screenshots/{datetime_string}.png"
    if not take_screenshot(screenshot_file):
        logger.error(f"Failed to take screenshot: {screenshot_file}")
        return

    logger.debug(f"Screenshot taken: {screenshot_file}")

    capture = Image.open(f"./captures/screenshots/{datetime_string}.png")

    # Check if the screenshot is identical to the previous one
    if bool(int(os.getenv('ENABLE_PERCEPTUAL_HASHING'))):
        phash = imagehash.phash(capture)
        if previous_phash is not None:
            if phash == previous_phash:
                logger.debug(f"Skipping identical frame: {datetime_string}")
                os.remove(screenshot_file)
                return

    # Check if the screenshot is similar to the previous one
    if bool(int(os.getenv('ENABLE_DIFFERENCE_THRESHOLD'))):
        dhash = imagehash.dhash(capture)
        if previous_dhash is not None:
            difference = dhash - previous_dhash
            logger.debug(f"Difference: {difference}")
            if difference < int(os.getenv('DIFFERENCE_THRESHOLD')):
                logger.debug(f"Skipping similar frame: {datetime_string}")
                os.remove(screenshot_file)
                return

    application_name = "Unknown"
    titlebar_str = ""
    title_text = ""

    if use_title_ocr:
        ocr_time = 0
        ocr_start_time = time.time()
        # Extract the titlebar and OCR it
        titlebar_str, title_text, application_name = ocr_titlebar(capture)

    else:
        titlebar_str = window_data['title']
        title_text = window_data['text']
        application_name = window_data['application_name']

    # Attempt to capture the URL from the titlebar
    url = ""
    url_time = 0
    url_partial = False
    if CAPTURE_BROWSER_URL:
        url, url_time, url_partial = capture_url(application_name, title_text, datetime_string)

    # Extract the content and OCR it
    content_str = ""
    should_ocr_content = True
    if LIVE_OCR_CONTENT:
        if application_name == "Unknown":
            if OCR_UNKNOWN_APPLICATIONS:
                content_str = ocr_content(capture)
            else:
                should_ocr_content = False
                logger.debug('Skipping OCR for unknown application')
        elif application_name in ocr_ignore_list:
            should_ocr_content = False
            logger.debug('Skipping OCR for ignored application ' + application_name)
        else:
            content_str = ocr_content(capture)

    ocr_time = time.time() - ocr_start_time
    capture_result = {
        'datetime': datetime_string,
        'file_path': screenshot_file,
        'ocr_title': title_text,
        'ocr_content': content_str,
        'application_name': application_name,
        'should_ocr_content': should_ocr_content,
        'ocr_time': ocr_time,
        'url': url,
        'url_time': url_time,
        'url_partial': url_partial
    }

    previous_dhash = dhash
    previous_phash = phash

    if DEBUG_OCR:
        os.makedirs(f"./captures/ocr", exist_ok=True)

        # Write OCR title to a file
        if len(titlebar_str) > 0:
            with open(f"./captures/ocr/{datetime_string}_title.txt", "w") as file:
                file.write(titlebar_str)

        # Write OCR content to a file
        if len(content_str) > 0:
            with open(f"./captures/ocr/{datetime_string}_content.txt", "w") as file:
                file.write(content_str)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f"Executed in {elapsed_time} seconds")

    return capture_result