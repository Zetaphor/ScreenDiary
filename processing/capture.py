import os
import time
from datetime import datetime
from PIL import Image
import imagehash
import hashlib
from dotenv import load_dotenv
from logger_config import get_logger
from util import in_dbus_ignore, in_ocr_ignore, get_application_remap, parse_application_name
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
LIVE_CAPTURE_BROWSER_URL = bool(int(os.getenv('LIVE_CAPTURE_BROWSER_URL')))
BROWSER_HISTORY_MATCH_TIME_RANGE = int(os.getenv('BROWSER_HISTORY_MATCH_TIME_RANGE'))

phash = None
dhash = None
md5hash = None
previous_dhash = None
previous_phash = None
previous_md5hash = None

def process_display(use_title_ocr=True, window_data=None):
    """
    Take a screenshot and process it to extract the titlebar and content
    If use_title_ocr is True, then OCR the titlebar and content, otherwise
    use window_data to set the window titlebar
    """
    global phash, dhash, md5hash, previous_dhash, previous_phash, previous_md5hash
    start_time = time.time()

    os.makedirs(f"./captures/screenshots", exist_ok=True)

    datetime_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_file = f"./captures/screenshots/{datetime_string}.png"
    if not take_screenshot(screenshot_file):
        logger.error(f"Failed to take screenshot: {screenshot_file}")
        return

    logger.debug(f"Screenshot taken: {screenshot_file}")

    capture = Image.open(f"./captures/screenshots/{datetime_string}.png")

    # Check if the screenshot is bit for bit identical to the previous one
    if bool(int(os.getenv('ENABLE_MD5_HASHING'))):
        with open(f"./captures/screenshots/{datetime_string}.png", 'rb') as file:
            data = file.read()
            md5hash = hashlib.md5(data).hexdigest()
            if previous_md5hash is not None:
                if md5hash == previous_md5hash:
                    logger.debug(f"Skipping identical frame {datetime_string} using MD5 Hashing")
                    os.remove(screenshot_file)
                    return

    # Check if the screenshot is identical to the previous one
    if bool(int(os.getenv('ENABLE_PERCEPTUAL_HASHING'))):
        phash = imagehash.phash(capture)
        if previous_phash is not None:
            if phash == previous_phash:
                logger.debug(f"Skipping identical frame {datetime_string} using Perceptual Hashing")
                os.remove(screenshot_file)
                return

    # Check if the screenshot is similar to the previous one
    if bool(int(os.getenv('ENABLE_DIFFERENCE_THRESHOLD'))):
        dhash = imagehash.dhash(capture)
        if previous_dhash is not None:
            difference = dhash - previous_dhash
            if difference < int(os.getenv('DIFFERENCE_THRESHOLD')):
                logger.debug(f"Skipping similar frame {datetime_string} using Difference Hashing. Detected Difference: {difference}")
                os.remove(screenshot_file)
                return

    application_name = "Unknown"
    remapped_name = None
    titlebar_str = ""
    title_text = ""
    ocr_time = 0
    ocr_start_time = time.time()

    if use_title_ocr:
        # Extract the titlebar and OCR it
        titlebar_str, title_text, application_name = ocr_titlebar(capture)
        remapped_name = get_application_remap(window_data, True)
        if remapped_name is not None:
            logger.debug(f"Remapped application name: {application_name} -> {remapped_name}")
    else:
        title_text, application_name = parse_application_name(window_data['caption'])
        remapped_name = get_application_remap(window_data, False)
        if remapped_name is not None:
            logger.debug(f"Remapped application name: {application_name} -> {remapped_name}")

    # Attempt to capture the URL from the titlebar
    url = ""
    url_time = 0
    url_partial = False
    if CAPTURE_BROWSER_URL and LIVE_CAPTURE_BROWSER_URL:
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
        else:
            if use_title_ocr:
                # We're using title OCR, so we should use the OCR ignore list
                if in_ocr_ignore(title_text):
                    should_ocr_content = False
                    logger.debug('Skipping OCR for ignored application ' + application_name + ' with title ' + title_text)
                else:
                    content_str = ocr_content(capture)
            else:
                if in_dbus_ignore(window_data):
                    should_ocr_content = False
                    logger.debug('Skipping OCR for ignored application ' + application_name + ' with title ' + title_text)
                else:
                    content_str = ocr_content(capture)
    else:
        logger.debug('Skipping OCR for ' + application_name)

    ocr_time = time.time() - ocr_start_time
    capture_result = {
        'datetime': datetime_string,
        'file_path': screenshot_file,
        'ocr_title': title_text,
        'ocr_content': content_str,
        'application_name': remapped_name if remapped_name is not None else application_name,
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